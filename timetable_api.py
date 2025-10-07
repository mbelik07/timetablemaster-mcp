# timetable_api.py
import requests
from typing import Dict, List

class TimetableMasterAPI:
    """
    A client for interacting with the TimetableMaster API.
    """
    def __init__(self, api_key: str, base_url: str):
        if not api_key:
            raise ValueError("API key cannot be empty.")
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, endpoint: str) -> Dict:
        """
        Internal helper to make GET requests to the TimetableMaster API.
        Includes error handling for common HTTP and API issues.
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            # Set a timeout for the request as a best practice
            response = requests.get(url, headers=self.headers, timeout=30)
            
            # Raise an exception for bad status codes (4xx client error or 5xx server error)
            response.raise_for_status()
            
            data = response.json()

            # Check the 'success' flag in the API's response body
            if not data.get('success'):
                error_message = data.get('error', {}).get('message', 'Unknown API error')
                error_code = data.get('error', {}).get('code', 'UNKNOWN_CODE')
                raise Exception(f"TimetableMaster API Error ({error_code}): {error_message}")
            
            return data['data']
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise Exception("Authentication Error: Invalid or missing API key.")
            elif e.response.status_code == 404:
                raise Exception("Not Found Error: The requested resource does not exist.")
            elif e.response.status_code == 429:
                raise Exception("Rate Limit Exceeded: Too many requests. Please try again later.")
            else:
                raise Exception(f"HTTP Error: {e.response.status_code} - {e.response.reason}")
        except requests.exceptions.ConnectionError as e:
            raise Exception(f"Connection Error: Could not connect to TimetableMaster API. {e}")
        except requests.exceptions.Timeout as e:
            raise Exception(f"Request Timeout: TimetableMaster API did not respond in time. {e}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"An unexpected request error occurred: {e}")
        except ValueError as e:
            raise Exception(f"Invalid JSON response from API: {e}")

    def list_timetables(self) -> List[Dict]:
        """
        Retrieves a list of all timetables for your organization.
        Returns a list of timetable summary objects.
        """
        print("Calling TimetableMaster API: list_timetables")
        data = self._make_request('timetables')
        return data.get('timetables', [])

    def get_timetable_data(self, timetable_id: str) -> Dict:
        """
        Retrieves complete timetable data for a specific timetable by ID.
        Args:
            timetable_id (str): The unique ID of the timetable.
        Returns a dictionary containing the detailed timetable data.
        """
        if not timetable_id:
            raise ValueError("Timetable ID cannot be empty.")
        print(f"Calling TimetableMaster API: get_timetable_data for ID '{timetable_id}'")
        return self._make_request(f'timetables/{timetable_id}')