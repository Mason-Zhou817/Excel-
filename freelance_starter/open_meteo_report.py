from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from freelance_starter.paths import ensure_parent, project_path

OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def load_cities(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"City config not found: {path}")
    cities = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(cities, list):
        raise ValueError("City config must be a list.")
    for city in cities:
        for field in ("name", "latitude", "longitude"):
            if field not in city:
                raise ValueError(f"City entry is missing field: {field}")
    return cities


def fetch_weather(
    city: dict[str, Any],
    *,
    session: Any = requests,
    timeout: int = 20,
) -> dict[str, Any]:
    response = session.get(
        OPEN_METEO_FORECAST_URL,
        params={
            "latitude": city["latitude"],
            "longitude": city["longitude"],
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "forecast_days": 3,
            "timezone": "auto",
        },
        headers={"User-Agent": "python-freelance-starter/1.0"},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    payload["city_name"] = city["name"]
    return payload


def normalize_current(payload: dict[str, Any]) -> dict[str, Any]:
    current = payload.get("current", {})
    units = payload.get("current_units", {})
    return {
        "city": payload["city_name"],
        "time": current.get("time"),
        "temperature": current.get("temperature_2m"),
        "temperature_unit": units.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "humidity_unit": units.get("relative_humidity_2m"),
        "wind_speed": current.get("wind_speed_10m"),
        "wind_speed_unit": units.get("wind_speed_10m"),
    }


def normalize_daily(payload: dict[str, Any]) -> list[dict[str, Any]]:
    daily = payload.get("daily", {})
    rows: list[dict[str, Any]] = []
    for index, date in enumerate(daily.get("time", [])):
        rows.append(
            {
                "city": payload["city_name"],
                "date": date,
                "temperature_max": value_at(daily.get("temperature_2m_max"), index),
                "temperature_min": value_at(daily.get("temperature_2m_min"), index),
                "precipitation_sum": value_at(daily.get("precipitation_sum"), index),
            }
        )
    return rows


def value_at(values: list[Any] | None, index: int) -> Any:
    if not values or index >= len(values):
        return None
    return values[index]


def build_weather_tables(
    cities: list[dict[str, Any]],
    *,
    session: Any = requests,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    current_rows: list[dict[str, Any]] = []
    daily_rows: list[dict[str, Any]] = []

    for city in cities:
        payload = fetch_weather(city, session=session)
        current_rows.append(normalize_current(payload))
        daily_rows.extend(normalize_daily(payload))

    return pd.DataFrame(current_rows), pd.DataFrame(daily_rows)


def write_weather_report(
    current_weather: pd.DataFrame,
    daily_forecast: pd.DataFrame,
    output_path: Path,
) -> None:
    ensure_parent(output_path)
    suffix = output_path.suffix.lower()
    if suffix == ".xlsx":
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            current_weather.to_excel(writer, sheet_name="current_weather", index=False)
            daily_forecast.to_excel(writer, sheet_name="daily_forecast", index=False)
    elif suffix == ".csv":
        current_weather.to_csv(output_path, index=False, encoding="utf-8-sig")
    else:
        raise ValueError("Output file must end with .csv or .xlsx")


def parse_args() -> argparse.Namespace:
    default_cities = project_path("projects", "03_api_report_tool", "input", "cities.json")
    default_output = project_path(
        "projects", "03_api_report_tool", "output", "weather_report.xlsx"
    )

    parser = argparse.ArgumentParser(
        description="Call Open-Meteo API and generate a weather report."
    )
    parser.add_argument("--cities", type=Path, default=default_cities)
    parser.add_argument("--output", type=Path, default=default_output)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cities = load_cities(args.cities)
    current_weather, daily_forecast = build_weather_tables(cities)
    write_weather_report(current_weather, daily_forecast, args.output)
    print(f"Weather report created for {len(cities)} city/cities: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
