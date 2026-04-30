import streamlit as st
from src.data_fetch import fetch_cpi_worldbank, fetch_exchange_rate
from src.preprocessing import merge_datasets, resample_fx_annual
from src.forecasting import forecast_series
import plotly.graph_objects as go

st.set_page_config(page_title="Kazakhstan Inflation Tracker", layout="wide")
st.title("Kazakhstan Inflation Tracker")


@st.cache_data
def load_data():
    cpi = fetch_cpi_worldbank()
    fx = fetch_exchange_rate()
    fx_annual = resample_fx_annual(fx)
    merged = merge_datasets(cpi, fx)
    cpi_forecast = forecast_series(cpi, "date", "cpi_yoy", periods=5)
    fx_forecast = forecast_series(fx_annual, "date", "kzt_per_usd", periods=5)
    return cpi, fx_annual, merged, cpi_forecast, fx_forecast


with st.spinner("Loading data..."):
    cpi_df, fx_annual_df, merged_df, cpi_forecast, fx_forecast = load_data()

tab1, tab2, tab3 = st.tabs(["CPI (Inflation)", "KZT/USD Exchange Rate", "Raw Data"])

with tab1:
    st.subheader("Annual CPI % Change (Year-over-Year)")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=cpi_df["date"], y=cpi_df["cpi_yoy"],
        mode="lines+markers", name="Actual"
    ))
    fig.add_trace(go.Scatter(
        x=cpi_forecast["ds"].dt.year, y=cpi_forecast["yhat"],
        mode="lines", name="Forecast", line=dict(dash="dash", color="orange")
    ))
    fig.add_trace(go.Scatter(
        x=list(cpi_forecast["ds"].dt.year) + list(cpi_forecast["ds"].dt.year[::-1]),
        y=list(cpi_forecast["yhat_upper"]) + list(cpi_forecast["yhat_lower"][::-1]),
        fill="toself", fillcolor="rgba(255,165,0,0.15)",
        line=dict(color="rgba(255,255,255,0)"),
        name="Confidence interval"
    ))
    fig.update_layout(xaxis_title="Year", yaxis_title="CPI YoY %", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("KZT per USD (Annual Average)")

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=fx_annual_df["date"], y=fx_annual_df["kzt_per_usd"],
        mode="lines+markers", name="Actual"
    ))
    fig2.add_trace(go.Scatter(
        x=fx_forecast["ds"].dt.year, y=fx_forecast["yhat"],
        mode="lines", name="Forecast", line=dict(dash="dash", color="orange")
    ))
    fig2.add_trace(go.Scatter(
        x=list(fx_forecast["ds"].dt.year) + list(fx_forecast["ds"].dt.year[::-1]),
        y=list(fx_forecast["yhat_upper"]) + list(fx_forecast["yhat_lower"][::-1]),
        fill="toself", fillcolor="rgba(255,165,0,0.15)",
        line=dict(color="rgba(255,255,255,0)"),
        name="Confidence interval"
    ))
    fig2.update_layout(xaxis_title="Year", yaxis_title="KZT per USD", hovermode="x unified")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Merged Annual Data (CPI + FX)")
    st.dataframe(merged_df, use_container_width=True)
