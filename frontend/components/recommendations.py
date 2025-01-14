import pandas as pd


def recommend_visualizations(df: pd.DataFrame):
    """
    Analyze the DataFrame to suggest best visualizations
    based on numeric vs. categorical columns and other heuristics.

    Returns a list of dicts, each describing one recommended chart, e.g.:
    [
      {
        "chart_type": "Bar Chart",
        "description": "Bar chart of total values by category",
        "x_col": "some_cat_column",
        "y_col": "some_num_column"
      },
      ...
    ]
    """
    recommendations = []

    # Identify column types
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = df.select_dtypes(exclude=["number"]).columns.tolist()
    # You could also detect date/time columns:
    # date_cols = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]

    # Simple heuristics:

    # 1) If at least one numeric col + one categorical col => bar chart
    if numeric_cols and cat_cols:
        # For demonstration, just pick the first of each:
        x_col = cat_cols[0]
        y_col = numeric_cols[0]
        recommendations.append(
            {
                "chart_type": "Bar Chart",
                "description": f"Bar chart: {y_col} grouped by {x_col}",
                "x_col": x_col,
                "y_col": y_col,
            }
        )

    # 2) If 2 or more numeric cols => scatter
    if len(numeric_cols) >= 2:
        # Just pick the first two for demonstration
        x_col = numeric_cols[0]
        y_col = numeric_cols[1]
        recommendations.append(
            {
                "chart_type": "Scatter Plot",
                "description": f"Scatter plot: {x_col} vs {y_col}",
                "x_col": x_col,
                "y_col": y_col,
            }
        )

    # 3) If exactly 1 numeric col => histogram
    if len(numeric_cols) == 1:
        recommendations.append(
            {
                "chart_type": "Histogram",
                "description": f"Distribution of {numeric_cols[0]}",
                "col": numeric_cols[0],
            }
        )

    # 4) If multiple numeric cols, a correlation heatmap might be interesting
    if len(numeric_cols) > 2:
        recommendations.append(
            {
                "chart_type": "Correlation Heatmap",
                "description": "Shows correlation among numeric columns",
            }
        )

    return recommendations
