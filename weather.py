"""Retrieve city forecasts using OpenWeatherMap and an environment-based API key."""

import os
import sys

import requests

GEOCODING_URL = "https://api.openweathermap.org/geo/1.0/direct"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
TIMEOUT = 20


def fetch_forecast(city, api_key):
    """Resolve a city to coordinates and return its forecast records."""
    city = city.strip()
    if not city:
        raise ValueError("A city name is required.")
    if not api_key or not api_key.strip():
        raise ValueError("Set the OPENWEATHER_API_KEY environment variable.")

    response = requests.get(
        GEOCODING_URL,
        params={"q": city, "appid": api_key, "limit": 1},
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    locations = response.json()
    if not locations:
        raise ValueError("No matching city was found.")
    location = locations[0]

    response = requests.get(
        FORECAST_URL,
        params={
            "lat": location["lat"],
            "lon": location["lon"],
            "appid": api_key,
            "units": "metric",
        },
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response.json()["list"]


def main():
    api_key = os.environ.get("OPENWEATHER_API_KEY", "")
    if not api_key.strip():
        print("Set the OPENWEATHER_API_KEY environment variable.", file=sys.stderr)
        return 1
    try:
        city = input("Enter city name: ")
        for record in fetch_forecast(city, api_key):
            print(
                record["dt_txt"], "->", record["main"]["temp"], "°C",
                record["weather"][0]["description"],
                "wind speed:", record["wind"]["speed"], "m/s",
            )
    except requests.RequestException:
        # Request exception strings may contain the API key in their URL.
        print("Weather request failed. Check your connection and API access.", file=sys.stderr)
        return 1
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1
    except (KeyError, IndexError, TypeError):
        print("The weather service returned an unexpected response.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
