"""
Plotting helpers for DataFrames

See the example notebook 'plotting-with-seaborn.ipynb' for examples on how to use
"""

import seaborn as sns
import warnings

CMIP6_SCENARIO_COLOURS = {
    "historical": "black",
    "ssp119": "#1e9583",
    "ssp126": "#1d3354",
    "ssp245": "#e9dc3d",
    "ssp370": "#f11111",
    "ssp370-lowNTCF-aerchemmip": "tab:pink",
    "ssp370-lowNTCF-gidden": "tab:red",
    "ssp434": "#63bce4",
    "ssp460": "#e78731",
    "ssp534-over": "#996dc8",
    "ssp585": "#830b22",
}


def long_data(self):
    """
    Return data in long form, particularly useful for plotting with seaborn

    Returns
    -------
    :obj:`pd.DataFrame`
            :obj:`pd.DataFrame` containing the data in 'long form' (i.e.
            on observation per row).
    """
    out = self.timeseries().stack()
    out.name = "value"
    out = out.to_frame().reset_index()

    return out


def lineplot(self, **kwargs):
    """
    Make a line plot via `seaborn's lineplot <https://seaborn.pydata.org/generated/seaborn.lineplot.html>`_

    Parameters
    ----------
    **kwargs
        Keyword arguments to be passed to ``seaborn.lineplot``. If none are passed,
        sensible defaults will be used.

    Returns
    -------
    :obj:`matplotlib.axes._subplots.AxesSubplot`
        Output of call to ``seaborn.lineplot``
    """
    plt_df = self.long_data()
    kwargs.setdefault("x", "time")
    kwargs.setdefault("y", "value")
    kwargs.setdefault("hue", "scenario")
    kwargs.setdefault("ci", "std")
    kwargs.setdefault("estimator", "median")

    ax = sns.lineplot(data=plt_df, **kwargs)

    return ax


def _deprecated_line_plot(self, **kwargs):
    """
    Make a line plot via `seaborn's lineplot <https://seaborn.pydata.org/generated/seaborn.lineplot.html>`_

    Deprecated: use :func`lineplot` instead

    Parameters
    ----------
    **kwargs
        Keyword arguments to be passed to ``seaborn.lineplot``. If none are passed,
        sensible defaults will be used.

    Returns
    -------
    :obj:`matplotlib.axes._subplots.AxesSubplot`
        Output of call to ``seaborn.lineplot``
    """
    warnings.warn("Use lineplot instead", DeprecationWarning)
    self.lineplot(**kwargs)


def inject_plotting_methods(cls):
    """
    Inject the plotting functions

    Parameters
    ----------
    cls
        Target class
    """
    methods = [
        ("long_data", long_data),
        ("lineplot", lineplot),
        ("line_plot", _deprecated_line_plot),  # for compatibility
    ]

    for name, f in methods:
        setattr(cls, name, f)
