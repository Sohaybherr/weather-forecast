import contextlib
import io
import unittest
from unittest.mock import Mock, patch

import requests

import weather


class ForecastTests(unittest.TestCase):
    def response(self, payload):
        response = Mock()
        response.json.return_value = payload
        return response

    @patch("weather.requests.get")
    def test_geocoding_coordinates_are_used_for_forecast(self, get):
        records = [{"dt_txt": "2026-11-22 12:00:00"}]
        get.side_effect = [self.response([{"lat": 33.57, "lon": -7.59}]), self.response({"list": records})]
        self.assertEqual(weather.fetch_forecast(" Casablanca ", "test-key"), records)
        self.assertEqual(get.call_args_list[0].kwargs["params"]["q"], "Casablanca")
        self.assertEqual(get.call_args_list[1].kwargs["params"], {"lat": 33.57, "lon": -7.59, "appid": "test-key", "units": "metric"})
        self.assertTrue(all(call.args[0].startswith("https://") for call in get.call_args_list))

    @patch("weather.requests.get")
    def test_invalid_input_does_not_make_requests(self, get):
        for city, key in [("", "test-key"), ("City", "")]:
            with self.assertRaises(ValueError):
                weather.fetch_forecast(city, key)
        get.assert_not_called()

    @patch("weather.requests.get")
    def test_unknown_city_stops_before_forecast(self, get):
        get.return_value = self.response([])
        with self.assertRaisesRegex(ValueError, "No matching city"):
            weather.fetch_forecast("unknown", "test-key")
        self.assertEqual(get.call_count, 1)

    @patch("weather.requests.get")
    def test_http_error_stops_before_parsing(self, get):
        get.return_value.raise_for_status.side_effect = requests.HTTPError("failure")
        with self.assertRaises(requests.HTTPError):
            weather.fetch_forecast("City", "test-key")
        get.return_value.json.assert_not_called()

    @patch.dict("os.environ", {"OPENWEATHER_API_KEY": "test-key"})
    @patch("builtins.input", return_value="Casablanca")
    @patch("weather.fetch_forecast")
    def test_cli_displays_forecast_fields(self, fetch, input_mock):
        fetch.return_value = [{"dt_txt": "2026-11-22 12:00:00", "main": {"temp": 21}, "weather": [{"description": "clear sky"}], "wind": {"speed": 3}}]
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(weather.main(), 0)
        for value in ["2026-11-22 12:00:00", "21", "clear sky", "3", "m/s"]:
            self.assertIn(value, output.getvalue())

    @patch.dict("os.environ", {"OPENWEATHER_API_KEY": "test-key"})
    @patch("builtins.input", return_value="City")
    @patch("weather.fetch_forecast", side_effect=requests.HTTPError("url?appid=secret-value"))
    def test_cli_does_not_disclose_key_in_request_errors(self, fetch, input_mock):
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            self.assertEqual(weather.main(), 1)
        self.assertNotIn("secret-value", output.getvalue())


if __name__ == "__main__":
    unittest.main()
