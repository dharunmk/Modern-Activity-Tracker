import requests
from dotenv import load_dotenv
import os
import hashlib
import base64
import hmac
import datetime

load_dotenv()

API_KEY = os.getenv("ATOMBERG_API_KEY")
REFRESH_TOKEN = os.getenv("ATOMBERG_REFRESH_TOKEN")
ACCESS_TOKEN = os.getenv("ATOMBERG_ACCESS_TOKEN")

def get_access_token():
    url = "https://api.developer.atomberg-iot.com/v1/get_access_token"
   
    # The API requires all these parameters
    headers = {
        'Authorization': f'Bearer {REFRESH_TOKEN}',
        'x-api-key': API_KEY
    }
   
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()['message']['access_token']
    except Exception as e:
        print(f"Request failed: {e}")
        return {"error": str(e)}



if __name__ == "__main__":
    access_token = get_access_token()
