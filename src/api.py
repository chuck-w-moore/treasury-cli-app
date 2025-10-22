import requests
from typing import List, Dict, Any


class TreasuryAPI:
    """
    A class to interact with the U.S. Treasury FiscalData API.
    """
    BASE_URL = ("https://api.fiscaldata.treasury.gov/services/api/"
                "fiscal_service")
    ENDPOINT = "/v2/accounting/od/avg_interest_rates"

    def fetch_rates_by_date(self, report_date: str) -> List[Dict[str, Any]]:
        """
        Fetches all average interest rates for a specific date.

        Args:
            report_date (str): The date to fetch data for,
                               in 'YYYY-MM-DD' format.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, where each
                                  dictionary represents a security and its
                                  rate, including the security type.

        Raises:
            requests.exceptions.RequestException: For network or HTTP errors.
            ValueError: If the API response is not valid JSON or is empty.
        """
        url = f"{self.BASE_URL}{self.ENDPOINT}"
        params = {
            'filter': f'record_date:eq:{report_date}',
            'sort': '-record_date,security_desc'
        }

        try:
            response = requests.get(url, params=params)
            # Raises an HTTPError for bad responses (4xx or 5xx)
            response.raise_for_status()

            data = response.json()
            if not data.get("data"):
                return []  # Return empty list if no data for that date

            # Clean and format the data, now including security_type_desc
            formatted_data = [
                {
                    "record_date": item["record_date"],
                    "security_type_desc": item["security_type_desc"],
                    "security_desc": item["security_desc"],
                    "rate": f'{float(item["avg_interest_rate_amt"]):.3f}%',
                }
                for item in data["data"]
            ]
            return formatted_data

        except requests.exceptions.JSONDecodeError:
            raise ValueError("Failed to decode JSON from response.")
        except requests.exceptions.RequestException as e:
            # Re-raise with a more informative message
            raise requests.exceptions.RequestException(
                f"API request failed: {e}"
                )
