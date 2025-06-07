import os
import json
import requests
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.auth.transport.requests import Request

load_dotenv()

# Load credentials JSON from environment variable
credentials_json = os.getenv("FIREBASE_CREDENTIALS_JSON")

if not credentials_json:
    raise ValueError("Missing FIREBASE_CREDENTIALS_JSON in environment variables")

credentials_dict = json.loads(credentials_json)

# Set up Google credentials for FCM v1
SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]
credentials = service_account.Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)
authed_session = Request()
credentials.refresh(authed_session)

# Your Firebase project ID
PROJECT_ID = credentials_dict["project_id"]

def send_push_notification(stock_list):
    # Compose the notification
    message_body = ", ".join([f"{s['symbol']} ({s['change']}%)" for s in stock_list])
    
    message = {
        "message": {
            "topic": "tradealerts",
            "notification": {
                "title": "Top 1-Day Trade Picks",
                "body": message_body
            }
        }
    }

    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json"
    }

    fcm_url = f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"
    response = requests.post(fcm_url, headers=headers, json=message)

    print("🔔 Notification sent!")
    print("Status Code:", response.status_code)
    print("Response:", response.text)