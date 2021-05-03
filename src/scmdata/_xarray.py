"""
Interface with `xarray <https://xarray.pydata.org/en/stable/index.html>`_
"""
import numpy as np
import xarray as xr

from .errors import NonUniqueMetadataError


def _to_xarray(run, dimensions, extras):
    timeseries = _get_timeseries_for_xr_dataset(run, dimensions, extras)
    non_dimension_extra_metadata = _get_other_metdata_for_xr_dataset(
        run, dimensions, extras
    )

    if extras:
        ids, ids_dimensions = _get_ids_for_xr_dataset(run, extras, dimensions)
    else:
        ids = None
        ids_dimensions = None

    for_xarray = _get_dataframe_for_xr_dataset(
        timeseries, dimensions, extras, ids, ids_dimensions
    )
    xr_ds = xr.Dataset.from_dataframe(for_xarray)

    if extras:
        xr_ds = _add_extras(xr_ds, ids, ids_dimensions, run)

    unit_map = (
        run.meta[["variable", "unit"]].drop_duplicates().set_index("variable")["unit"]
    )
    xr_ds = _add_units(xr_ds, unit_map)
    xr_ds = _rename_variables(xr_ds)
    xr_ds = _add_scmdata_metadata(xr_ds, non_dimension_extra_metadata)

    return xr_ds


def _get_timeseries_for_xr_dataset(run, dimensions, extras):
    for d in dimensions:
        vals = sorted(run.meta[d].unique())
        if not all([isinstance(v, str) for v in vals]) and np.isnan(vals).any():
            raise AssertionError("nan in dimension: `{}`".format(d))

    try:
        timeseries = run.timeseries(dimensions + extras + ["variable"])
    except NonUniqueMetadataError as exc:
        error_msg = (
            "dimensions: `{}` and extras: `{}` do not uniquely define the "
            "timeseries, please add extra dimensions and/or extras".format(
                dimensions, extras
            )
        )
        raise ValueError(error_msg) from exc

    timeseries.columns = run.time_points.as_cftime()

    return timeseries


def _get_other_metdata_for_xr_dataset(run, dimensions, extras):
    other_dimensions = list(
        set(run.meta.columns) - set(dimensions) - set(extras) - {"variable", "unit"}
    )
    other_metdata = run.meta[other_dimensions].drop_duplicates()
    if other_metdata.shape[0] > 1 and not other_metdata.empty:
        error_msg = (
            "Other metadata is not unique for dimensions: `{}` and extras: `{}`. "
            "Please add meta columns with more than one value to dimensions or "
            "extras.\nNumber of unique values in each column:\n{}.\n"
            "Existing values in the other metadata:\n{}.".format(
                dimensions,
                extras,
                other_metdata.nunique(),
                other_metdata.drop_duplicates(),
            )
        )
        raise ValueError(error_msg)

    return other_metdata


def _get_ids_for_xr_dataset(run, extras, dimensions):
    # these loops could be very slow with lots of extras and dimensions...
    ids_dimensions = {}
    for extra in extras:
        for col in dimensions:
            if _many_to_one(run.meta, extra, col):
                dim_col = col
                break
        else:
            dim_col = "_id"

        ids_dimensions[extra] = dim_col

    ids = run.meta[extras].drop_duplicates()
    ids["_id"] = range(ids.shape[0])
    ids = ids.set_index(extras)

    return ids, ids_dimensions


def _many_to_one(df, col1, col2):
    """
    Check if there is a many to one mapping between col2 and col1
    """
    # thanks https://stackoverflow.com/a/59091549
    checker = df[[col1, col2]].drop_duplicates()

    max_count = checker.groupby(col2).count().max()[0]
    if max_count < 1:  # pragma: no cover # emergency valve
        raise AssertionError

    return max_count == 1


def _get_dataframe_for_xr_dataset(timeseries, dimensions, extras, ids, ids_dimensions):
    timeseries = timeseries.reset_index()

    add_id_dimension = extras and "_id" in set(ids_dimensions.values())
    if add_id_dimension:
        timeseries = (
            timeseries.set_index(ids.index.names)
            .join(ids)
            .reset_index(drop=True)
            .set_index(dimensions + ["variable", "_id"])
        )
    else:
        timeseries = timeseries.set_index(dimensions + ["variable"])
        if extras:
            timeseries = timeseries.drop(extras, axis="columns")

    timeseries.columns.names = ["time"]

    if (
        len(timeseries.index.unique()) != timeseries.shape[0]
    ):  # pragma: no cover # emergency valve
        # shouldn't be able to get here because any issues should be caught
        # by initial creation of timeseries but just in case
        raise AssertionError("something not unique")

    for_xarray = (
        timeseries.T.stack(dimensions + ["_id"])
        if add_id_dimension
        else timeseries.T.stack(dimensions)
    )

    return for_xarray


def _add_extras(xr_ds, ids, ids_dimensions, run):
    # this loop could also be slow...
    extra_coords = {}
    for extra, id_dimension in ids_dimensions.items():
        if id_dimension in ids:
            ids_extra = ids.reset_index().set_index(id_dimension)
        else:
            ids_extra = (
                run.meta[[extra, id_dimension]]
                .drop_duplicates()
                .set_index(id_dimension)
            )

        extra_coords[extra] = (
            id_dimension,
            ids_extra[extra].loc[xr_ds[id_dimension].values],
        )

    xr_ds = xr_ds.assign_coords(extra_coords)

    return xr_ds


def _add_units(xr_ds, unit_map):
    for data_var in xr_ds.data_vars:
        unit = unit_map[data_var]
        xr_ds[data_var].attrs["units"] = unit

    return xr_ds


def _var_to_nc(var):
    # TODO: remove renaming in this module
    return var.replace("|", "__").replace(" ", "_")


def _rename_variables(xr_ds):
    name_mapping = {}
    for data_var in xr_ds.data_vars:
        serialised_name = _var_to_nc(data_var)
        name_mapping[data_var] = serialised_name
        xr_ds[data_var].attrs["long_name"] = data_var

    xr_ds = xr_ds.rename_vars(name_mapping)

    return xr_ds


def _add_scmdata_metadata(xr_ds, others):
    for col in others:
        vals = others[col].unique()
        if len(vals) > 1:  # pragma: no cover # emergency valve
            # should have already been caught...
            raise AssertionError("More than one value for meta: {}".format(col))

        xr_ds.attrs["_scmdata_metadata_{}".format(col)] = vals[0]

    return xr_ds
