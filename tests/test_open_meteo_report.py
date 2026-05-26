from __future__ import annotations

from typing import Any

import requests

from freelance_starter.open_meteo_report import (
    build_weather_tables,
    fetch_weather,
    normalize_current,
    normalize_daily,
)


SAMPLE_PAYLOAD = {
    "city_name": "Shanghai",
    "current": {
        "time": "2026-05-17T16:00",
        "temperature_2m": 24.5,
        "relative_humidity_2m": 68,
        "wind_speed_10m": 12.3,
    },
    "current_units": {
        "temperature_2m": "degC",
        "relative_humidity_2m": "%",
        "wind_speed_10m": "km/h",
    },
    "daily": {
        "time": ["2026-05-17", "2026-05-18"],
        "temperature_2m_max": [26.0, 27.0],
        "temperature_2m_min": [19.0, 20.0],
        "precipitation_sum": [0.2, 0.0],
    },
}


class FakeResponse:
    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, Any]:
        payload = dict(SAMPLE_PAYLOAD)
        payload.pop("city_name")
        return payload


class FakeSession:
    def get(self, *args: Any, **kwargs: Any) -> FakeResponse:
        return FakeResponse()


class FlakySession:
    def __init__(self) -> None:
        self.calls = 0

    def get(self, *args: Any, **kwargs: Any) -> FakeResponse:
        self.calls += 1
        if self.calls == 1:
            raise requests.Timeout("temporary timeout")
        return FakeResponse()


class FailingSession:
    def get(self, *args: Any, **kwargs: Any) -> FakeResponse:
        raise requests.Timeout("network timeout")


def test_normalize_current_weather() -> None:
    row = normalize_current(SAMPLE_PAYLOAD)

    assert row["city"] == "Shanghai"
    assert row["temperature"] == 24.5
    assert row["humidity_unit"] == "%"


def test_normalize_daily_forecast_rows() -> None:
    rows = normalize_daily(SAMPLE_PAYLOAD)

    assert len(rows) == 2
    assert rows[0]["date"] == "2026-05-17"
    assert rows[1]["temperature_max"] == 27.0


def test_build_weather_tables_uses_city_name_from_config() -> None:
    current_weather, daily_forecast, api_errors = build_weather_tables(
        [{"name": "Shanghai", "latitude": 31.23, "longitude": 121.47}],
        session=FakeSession(),
    )

    assert current_weather.loc[0, "city"] == "Shanghai"
    assert len(daily_forecast) == 2
    assert api_errors.empty


def test_fetch_weather_retries_transient_timeout() -> None:
    session = FlakySession()

    payload = fetch_weather(
        {"name": "Shanghai", "latitude": 31.23, "longitude": 121.47},
        session=session,
        retries=1,
        backoff_seconds=0,
    )

    assert session.calls == 2
    assert payload["city_name"] == "Shanghai"


def test_build_weather_tables_records_failed_city() -> None:
    current_weather, daily_forecast, api_errors = build_weather_tables(
        [{"name": "Shanghai", "latitude": 31.23, "longitude": 121.47}],
        session=FailingSession(),
        retries=0,
        backoff_seconds=0,
    )

    assert current_weather.empty
    assert daily_forecast.empty
    assert api_errors.loc[0, "city"] == "Shanghai"
    assert api_errors.loc[0, "attempts"] == 1
