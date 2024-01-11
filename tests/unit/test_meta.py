"""Tests for ScmRun.meta and related functionality."""

import pandas as pd
import numpy as np

import scmdata

def test_preserve_type():
    df = pd.DataFrame({"unit": [np.nan, np.nan], "variable": ["1", "2"], 2015: [1., 2.]}, dtype=str)
    run = scmdata.run.BaseScmRun(pd.DataFrame(df))
    assert run.meta.dtypes["variable"] in (str, object)
    assert run.meta.dtypes["unit"] in (str, object)
