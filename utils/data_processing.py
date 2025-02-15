import pandas as pd

# ------------------------------------------------------------------------
# Correct the parquet file column names | Remove invalide character
# ------------------------------------------------------------------------

def correct_parquet_cols(*dfs):
    """
    Removes invalid characters from column names in one or more Pandas DataFrames.

    This function supports:
    - A single DataFrame: Returns the cleaned DataFrame.
    - Multiple DataFrames: Returns them as separate values, allowing unpacking.

    Parameters:
    *dfs (pd.DataFrame): One or more Pandas DataFrames.

    Returns:
    - pd.DataFrame: If a single DataFrame is passed.
    - Tuple[pd.DataFrame, ...]: If multiple DataFrames are passed.

    Example Usage:
    ---------------
    df1 = pd.DataFrame(columns=["col+-+name", "col-+-value"])
    df1 = correct_parquet_cols(df1)  #  Single DF

    df1, df2 = correct_parquet_cols(df1, df2)  #  Multiple DFs
    """

    if not all(isinstance(df, pd.DataFrame) for df in dfs):
        raise TypeError("All arguments must be Pandas DataFrames")

    cleaned_dfs = tuple(
        df.rename(columns=lambda col: col.replace("+-+", ".").replace("-+-", " "))
        for df in dfs
    )

    return cleaned_dfs if len(cleaned_dfs) > 1 else cleaned_dfs[0]
# ------------------------------------------------------------------------END
