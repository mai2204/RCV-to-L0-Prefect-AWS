# Common/module/convert_functions.py

import pandas as pd

def convert_null(series: pd.Series):
    return None  # or series.apply(lambda x: None)

def convert_datetime(series: pd.Series):
    return pd.to_datetime(series, errors="coerce")