# Kazakhstan Inflation Tracker

An interactive web app that tracks Kazakhstan's inflation (CPI) and the KZT/USD exchange rate, with five-year forecasts and confidence intervals.

Built with Python, Streamlit, Plotly, and Prophet.

## Features

- **CPI (Inflation):** annual year-over-year % change, with a 5-year forecast
- **KZT/USD Exchange Rate:** annual average rate, with a 5-year forecast
- **Forecast confidence intervals** shown as shaded bands on both charts
- **Raw Data tab:** the merged annual CPI + exchange rate dataset
- **Cached data loading**, so data is not re-fetched and re-processed on every interaction

## How It Works

1. **Fetch:** CPI data is pulled from the World Bank API, along with KZT/USD exchange rate data.
2. **Preprocess:** exchange rates are resampled to annual averages and merged with the CPI data.
3. **Forecast:** a Prophet model is fitted to each series and predicts the next 5 years. Yearly, weekly, and daily seasonality are disabled because the data is annual.
4. **Visualize:** results are displayed in an interactive Streamlit dashboard with Plotly charts.

### Design note

Training data is limited to years from 2000 onward. Earlier years include post-Soviet hyperinflation, which would distort the forecasts. This cutoff is configurable through the `start_year` parameter in `forecast_series`.

## Project Structure

```
.
├── app.py                  # Streamlit app
└── src/
    ├── data_fetch.py       # Fetches CPI and exchange rate data
    ├── preprocessing.py    # Resampling and merging datasets
    └── forecasting.py      # Prophet forecasting
```

## Getting Started

### Prerequisites

- Python 3.9+

### Installation

```bash
git clone <your-repo-url>
cd <your-repo-folder>
pip install streamlit plotly pandas prophet
```

### Run the app

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal (usually http://localhost:8501).

## Limitations

- Forecasts are based on a small number of annual data points, so the confidence intervals can be wide.
- Prophet is designed for higher-frequency time series; here it is used on yearly data as a simple baseline.
- Forecasts are for learning and exploration, not financial or economic advice.

## Future Improvements

- Compare Prophet against other forecasting models (e.g. ARIMA)
- Add more indicators (interest rates, oil prices)
- Add data export

## Data Sources

- [World Bank Open Data](https://data.worldbank.org/) for CPI
- KZT/USD exchange rate data (add your source here)
