"""Build the 2025 Virginia-origin BTS on-time performance dataset."""
from __future__ import annotations

import io
import zipfile
from pathlib import Path

import pandas as pd

YEAR = 2025
BASE_URL = "https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{year}_{month}.zip"
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"

KEEP = [
    "Year", "Month", "DayofMonth", "DayOfWeek", "FlightDate",
    "Reporting_Airline", "Flight_Number_Reporting_Airline",
    "Origin", "OriginState", "Dest", "DestState",
    "CRSDepTime", "DepTime", "DepDelay", "DepDel15", "TaxiOut",
    "CRSArrTime", "ArrTime", "ArrDelay", "ArrDel15", "TaxiIn",
    "CRSElapsedTime", "ActualElapsedTime", "AirTime", "Distance",
    "Cancelled", "CancellationCode", "Diverted", "CarrierDelay",
    "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay",
]


def download_month(month: int) -> Path:
    RAW.mkdir(parents=True, exist_ok=True)
    target = RAW / f"bts_{YEAR}_{month:02d}.zip"
    if target.exists():
        return target
    import requests
    url = BASE_URL.format(year=YEAR, month=month)
    response = requests.get(url, timeout=180)
    response.raise_for_status()
    target.write_bytes(response.content)
    return target


def read_month(path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as archive:
        csv_name = next(n for n in archive.namelist() if n.lower().endswith(".csv"))
        with archive.open(csv_name) as handle:
            frame = pd.read_csv(handle, low_memory=False)
    missing = [column for column in KEEP if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing expected BTS columns in {path.name}: {missing}")
    return frame.loc[frame["OriginState"].eq("VA"), KEEP].copy()


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    frames = [read_month(download_month(month)) for month in range(1, 13)]
    data = pd.concat(frames, ignore_index=True)
    valid_arrival = data["Cancelled"].eq(0) & data["Diverted"].eq(0)
    data["MinutesRecovered"] = (data["DepDelay"] - data["ArrDelay"]).where(valid_arrival)
    data["Delayed15"] = data["ArrDelay"].ge(15).astype("Int64").where(valid_arrival)
    data.sort_values(["FlightDate", "Origin", "Reporting_Airline"], inplace=True)
    data.to_csv(DATA / "va_flights_2025.csv.gz", index=False, compression="gzip")
    data.head(1000).to_csv(DATA / "va_flights_2025_sample.csv", index=False)
    print(f"Wrote {len(data):,} Virginia-origin flights and {len(data.columns)} columns")


if __name__ == "__main__":
    main()
