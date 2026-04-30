import requests
import pandas as pd
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import date
from typing import Optional
from dateutil.relativedelta import relativedelta

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def fetch_cpi_worldbank(country_code: str = "KZ", cache: bool = True) -> pd.DataFrame:
    """Fetch annual CPI data for Kazakhstan from World Bank API."""
    cache_path = RAW_DIR / f"cpi_{country_code}.json"

    if cache and cache_path.exists():
        with open(cache_path) as f:
            data = json.load(f)
    else:
        url = (
            f"https://api.worldbank.org/v2/country/{country_code}"
            f"/indicator/FP.CPI.TOTL.ZG?format=json&per_page=100"
        )
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        if cache:
            with open(cache_path, "w") as f:
                json.dump(data, f)

    records = data[1]
    df = pd.DataFrame([
        {"date": int(r["date"]), "cpi_yoy": r["value"]}
        for r in records
        if r["value"] is not None
    ])
    df = df.sort_values("date").reset_index(drop=True)
    return df


def _fetch_nbk_rate_on_date(d: date) -> Optional[float]:
    """Fetch USD/KZT rate from NBK for a specific date."""
    date_str = d.strftime("%d.%m.%Y")
    url = f"https://nationalbank.kz/rss/get_rates.cfm?fdate={date_str}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    for item in root.findall("item"):
        title = item.findtext("title", "").strip()
        if title == "USD":
            val = item.findtext("description", "").strip()
            quant = item.findtext("quant", "1").strip()
            return float(val) / float(quant)
    return None


def fetch_exchange_rate(start_year: int = 2000, cache: bool = True) -> pd.DataFrame:
    """
    Fetch monthly KZT/USD exchange rates from National Bank of Kazakhstan.
    Samples the first business day of each month from start_year to today.
    """
    cache_path = RAW_DIR / "fx_USD_KZT_nbk.json"

    if cache and cache_path.exists():
        with open(cache_path) as f:
            records = json.load(f)
        df = pd.DataFrame(records)
        df["date"] = pd.to_datetime(df["date"])
        return df

    records = []
    current = date(start_year, 1, 1)
    end = date.today()

    while current <= end:
        rate = _fetch_nbk_rate_on_date(current)
        if rate is not None:
            records.append({"date": current.isoformat(), "kzt_per_usd": rate})
        current += relativedelta(months=1)

    if cache:
        with open(cache_path, "w") as f:
            json.dump(records, f)

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    return df
