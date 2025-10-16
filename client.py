# client.py

import requests

from config import BASE_URL, HEADERS


def post(endpoint: str, data: dict) -> dict:
    url = f"{BASE_URL}{endpoint}"
    #print(url)
    #print(data)
    # exit()
    try:
        response = requests.post(url, json=data, headers=HEADERS, timeout=100)
        response.raise_for_status()
        return {
            "success": True,
            "status_code": response.status_code,
            "response": response.json() if response.headers.get("Content-Type", "").startswith("application/json") else response.text
        }
    except requests.RequestException as e:
        return {"success": False, "error": str(e)}
