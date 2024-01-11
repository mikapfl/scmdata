"""Tests for ScmRun.meta."""

import numpy as np
import pandas as pd

import scmdata


def test_correct_type_meta():
    df = pd.DataFrame(
        {
            "unit": pd.Series([np.nan, np.nan], dtype=str),
            "variable": pd.Series(["1", "2"], dtype=str),
            "extra": pd.Series([1, 2], dtype=int),
            2015: pd.Series([1.0, 2.0], dtype=float),
        },
    )
    run = scmdata.run.BaseScmRun(pd.DataFrame(df))
    assert run.meta.dtypes["extra"] == int
    assert run.meta.dtypes["variable"] in (str, object)
    assert run.meta.dtypes["unit"] in (str, object)
