import json
from unittest.mock import patch

from django.test import TestCase
from requests.exceptions import HTTPError


class MockCookies:
    
    def get_dict(self):
        return {}


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.content = str(json_data)
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code > 299:
            raise HTTPError(f'Error code: {self.status_code}')

    @property
    def text(self):
        return str(self.content)

    @property
    def cookies(self):
        return MockCookies()


class WeatherTestCase(TestCase):

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    @patch('requests.get')
    def test_weather_success(self, mock_requests_get):
        with open(
            'weather/test/success_payload.json'
        ) as json_response_success:
            expected_result = json.load(json_response_success)

        mock_requests_get.return_value = MockResponse(
            expected_result, 200
        )
        response = self.client.get('/weather')
        self.assertTemplateUsed(response, 'weather/weather.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains (
            response,
            expected_result["location"]["name"]
        )

    @patch('requests.get')
    def test_weather_fail(self, mock_requests_get):
        with open(
            'weather/test/fail_payload.json'
        ) as json_response_success:
            expected_result = json.load(json_response_success)

        mock_requests_get.return_value = MockResponse(
            expected_result, 200
        )
        response = self.client.get('/weather')
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            expected_result["error"]["info"]
        )
        self.assertTemplateUsed(response, 'weather/weather.html')
    
    @patch('requests.get')
    def test_weather_error(self, mock_requests_get):
        mock_requests_get.return_value = MockResponse(
            {}, 404
        )
        response = self.client.get('/weather')
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Looks like our services are currently offline"
        )
        self.assertTemplateUsed(response, 'weather/weather.html')