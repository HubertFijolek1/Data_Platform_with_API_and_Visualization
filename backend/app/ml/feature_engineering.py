import pandas as pd


def add_new_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    Example function that creates or modifies columns in the DataFrame.
    e.g. constructing a new feature from existing columns
    It will be changed in the nearest future.
    """
    numeric_cols = df.select_dtypes(include=["float", "int"]).columns.tolist()
    if len(numeric_cols) >= 2:
        df["feat_sum"] = df[numeric_cols[0]] + df[numeric_cols[1]]
    return df
