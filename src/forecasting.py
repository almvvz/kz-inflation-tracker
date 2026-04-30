import pandas as pd
from prophet import Prophet


def forecast_series(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    periods: int = 5,
    start_year: int = 2000,
) -> pd.DataFrame:
    """
    Fit a Prophet model and return forecast dataframe.

    Parameters
    ----------
    df         : DataFrame with date and value columns
    date_col   : column name for year integers
    value_col  : column name for the target variable
    periods    : number of future yearly periods to forecast
    start_year : exclude years before this to avoid distortion from outliers
                 (e.g. post-Soviet hyperinflation years)

    Returns
    -------
    DataFrame with columns: ds, yhat, yhat_lower, yhat_upper
    """
    filtered = df[df[date_col] >= start_year].copy()

    prophet_df = pd.DataFrame({
        "ds": pd.to_datetime(filtered[date_col].astype(str), format="%Y"),
        "y": filtered[value_col].astype(float),
    })

    model = Prophet(
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=False,
    )
    model.fit(prophet_df)

    # Use YS (year start) so future dates stay Jan-1, matching historical format
    future = model.make_future_dataframe(periods=periods, freq="YS")
    forecast = model.predict(future)

    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
