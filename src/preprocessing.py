import pandas as pd


def resample_fx_annual(fx_df: pd.DataFrame) -> pd.DataFrame:
    """Resample daily/monthly FX data to annual averages."""
    df = fx_df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")
    annual = df["kzt_per_usd"].resample("YE").mean().reset_index()
    annual["date"] = annual["date"].dt.year
    annual.columns = ["date", "kzt_per_usd"]
    return annual


def merge_datasets(cpi_df: pd.DataFrame, fx_df: pd.DataFrame) -> pd.DataFrame:
    """Merge CPI and FX dataframes on year."""
    fx_annual = resample_fx_annual(fx_df)
    merged = pd.merge(cpi_df, fx_annual, on="date", how="inner")
    return merged

