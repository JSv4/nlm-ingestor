import json
import pprint

import requests


def submit_pdf(file_path: str, api_url: str, api_key: str):
    """
    Submits a PDF file to the specified API endpoint with calculate_opencontracts_data set to True.

    Args:
        file_path (str): The path to the PDF file to be submitted.
        api_url (str): The URL of the API endpoint.
        api_key (str): The API key for authorization.

    Returns:
        dict: The JSON response from the server.
    """
    headers = {'API_KEY': api_key}
    print(f"Header: {headers}")
    files = {'file': open(file_path, 'rb')}
    params = {'calculate_opencontracts_data': 'yes'}  # Ensures calculate_opencontracts_data is set to True

    response = requests.post(api_url, headers=headers, files=files, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


# Usage example
if __name__ == "__main__":
    api_url = 'http://localhost:5001/api/parseDocument'
    api_key = 'abc123'
    file_path = 'C:\\Users\\jscru\\Downloads\\sample.pdf'

    try:
        response = submit_pdf(file_path, api_url, api_key)
        with open("sample_nlm_ingestor_output.json", "w") as f:
            f.write(json.dumps(response, indent=4))
    except Exception as e:
        print(f"An error occurred: {e}")
