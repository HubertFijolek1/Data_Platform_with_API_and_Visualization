import pandas as pd
from typing import Optional
from .feature_engineering import add_new_feature


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Example preprocessing function that will be expanded:
    - handle missing values
    - encode categorical features
    - scale/normalize data
    """
    df_cleaned = df.dropna()
    df_cleaned = add_new_feature(df_cleaned)
    return df_cleaned
