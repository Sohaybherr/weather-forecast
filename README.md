# Weather Forecast Client

## Abstract

This project implements a command-line weather forecast client in Python. A city name is resolved into geographic coordinates through the OpenWeatherMap geocoding service. These coordinates are subsequently used to retrieve forecast records and display their timestamps, temperatures, weather descriptions, and wind speeds. The implementation illustrates a sequential API integration workflow using HTTP requests and structured JSON responses.

## Academic Objectives

- Translate a user-supplied location into a coordinate representation.
- Construct parameterized HTTP requests to two related API endpoints.
- Interpret nested JSON structures and extract selected meteorological fields.
- Separate configuration from source code and handle common input and network failures.

## Methodology

1. Read a city name from standard input and obtain an API key from the process environment.
2. Submit the city to the geocoding endpoint, requesting one candidate location.
3. Extract the latitude and longitude of the first returned candidate.
4. Request the forecast for those coordinates using metric units.
5. Iterate over the returned records and print the timestamp, temperature in degrees Celsius, description, and wind speed in metres per second.

The program retrieves forecasts produced by an external service. It does not train a predictive model or calculate forecasts independently.

## Implementation Structure

| File | Role |
| --- | --- |
| `weather.py` | Geocoding, forecast retrieval, input handling, and console output |
| `requirements.txt` | Direct Python dependency |
| `.env.example` | Example configuration variable; no credentials are distributed |
| `tests/test_weather.py` | Isolated tests with simulated HTTP responses |

`fetch_forecast(city, api_key)` contains the retrieval workflow. `main()` manages interactive execution and reports input, response, and connection failures. Requests use HTTPS and a timeout. HTTP status failures are checked before response data is processed.

## Execution Environment

The program requires Python 3, the `requests` package, internet access, and an OpenWeatherMap API key authorized for the endpoints used.

```sh
python -m pip install -r requirements.txt
```

Set the key in the same shell used to launch the program.

PowerShell:

```powershell
$env:OPENWEATHER_API_KEY = "your_api_key"
python weather.py
```

Linux or macOS:

```sh
export OPENWEATHER_API_KEY="your_api_key"
python weather.py
```

Enter a city name when prompted. A more specific location, such as `Casablanca,MA`, can reduce ambiguity. `.env.example` documents the variable; the application does not automatically load `.env` files.

## Validation

```sh
python -m unittest discover -s tests -v
```

The tests simulate service responses to examine request parameters, response extraction, missing configuration, unknown locations, HTTP failures, and command-line output. They require no real key and make no network calls. They do not establish live API availability or forecast accuracy.

## Limitations

- The first geocoding candidate is selected without an interactive disambiguation step.
- Available forecast records, timestamp representation, and coverage depend on the external service response.
- There is no caching, persistent storage, visualization, retry policy, or offline operation.
- Live API behavior and meteorological accuracy have not been evaluated for this repository.
- Dependency versions are not pinned; the repository does not define a fully reproducible software environment.

## Source Context

This repository develops a local Python weather exercise into a standalone project. The original retrieval sequence and displayed fields are retained. Configuration was moved from an embedded API key to an environment variable, and request validation and isolated tests were added. Related coursework is collected in [Programming Projects and Academic Exercises](https://github.com/Sohaybherr/local-projects).
