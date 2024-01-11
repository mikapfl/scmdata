"""Tests for ScmRun.meta."""

import pandas as pd
import numpy as np

import scmdata

def test_correct_type_meta():
    df = pd.DataFrame({"unit": [np.nan, np.nan], "variable": ["1", "2"], 2015: [1., 2.]}, dtype=str)
    run = scmdata.run.BaseScmRun(pd.DataFrame(df))
    assert run.meta.dtypes["variable"] in (str, object)
    assert run.meta.dtypes["unit"] in (str, object)
