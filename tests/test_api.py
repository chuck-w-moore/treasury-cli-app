import pytest
import requests
from unittest.mock import patch, MagicMock
from src.api import TreasuryAPI

@pytest.fixture
def api_client():
    """Fixture to create an instance of the TreasuryAPI."""
    return TreasuryAPI()

@pytest.fixture
def mock_api_response():
    """Fixture to provide a sample successful API response."""
    return {
        "data": [
            {
                "record_date": "2023-09-30",
                "security_type_desc": "Marketable",
                "security_desc": "Treasury Bills",
                "avg_interest_rate_amt": "4.187",
            },
            {
                "record_date": "2023-09-30",
                "security_type_desc": "Marketable",
                "security_desc": "Treasury Notes",
                "avg_interest_rate_amt": "3.112",
            }
        ],
        "meta": {"count": 2, "total-pages": 1}
    }

@patch('src.api.requests.get')
def test_fetch_rates_success(mock_get, api_client, mock_api_response):
    """
    Tests a successful API call and data transformation.
    """
    # Configure the mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_api_response
    mock_get.return_value = mock_response

    # Call the method
    report_date = "2023-09-30"
    rates = api_client.fetch_rates_by_date(report_date)

    # Check that requests.get was called correctly
    expected_url = f"{api_client.BASE_URL}{api_client.ENDPOINT}"
    expected_params = {
        'filter': f'record_date:eq:{report_date}',
        'sort': '-record_date,security_desc'
    }
    mock_get.assert_called_once_with(expected_url, params=expected_params)

    # Check the transformed data
    assert len(rates) == 2
    assert rates[0] == {
        "record_date": "2023-09-30",
        "security_type_desc": "Marketable",
        "security_desc": "Treasury Bills",
        "rate": "4.187%",
    }
    assert rates[1]["security_desc"] == "Treasury Notes"
    assert rates[1]["rate"] == "3.112%"

@patch('src.api.requests.get')
def test_fetch_rates_http_error(mock_get, api_client):
    """
    Tests that an HTTP error from requests.get is caught and re-raised.
    """
    # Configure the mock to raise an HTTPError
    mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")

    # Use pytest.raises to assert that the specific exception is raised
    with pytest.raises(requests.exceptions.RequestException, match="API request failed"):
        api_client.fetch_rates_by_date("2023-09-30")

@patch('src.api.requests.get')
def test_fetch_rates_no_data_found(mock_get, api_client):
    """
    Tests that an empty list is returned when the API finds no data.
    """
    # Configure the mock response for "no data"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    mock_get.return_value = mock_response

    rates = api_client.fetch_rates_by_date("2023-01-01")

    # Assert an empty list is returned
    assert rates == []

@patch('src.api.requests.get')
def test_fetch_rates_json_decode_error(mock_get, api_client):
    """
    Tests handling of a malformed JSON response.
    """
    # Configure the mock to raise a JSONDecodeError
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = requests.exceptions.JSONDecodeError("msg", "doc", 0)
    mock_get.return_value = mock_response

    # Assert that our custom ValueError is raised
    with pytest.raises(ValueError, match="Failed to decode JSON from response."):
        api_client.fetch_rates_by_date("2023-09-30")