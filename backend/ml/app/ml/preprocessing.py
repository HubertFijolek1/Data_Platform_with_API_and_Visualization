import pandas as pd

from .feature_engineering import add_new_feature


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df_cleaned = df.dropna()
    df_cleaned = add_new_feature(df_cleaned)
    return df_cleaned
