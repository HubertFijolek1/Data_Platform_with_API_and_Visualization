import pandas as pd
from typing import Optional

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Example preprocessing function that will be expanded:
    - handle missing values
    - encode categorical features
    - scale/normalize data
    """
    df_cleaned = df.dropna()
    return df_cleaned