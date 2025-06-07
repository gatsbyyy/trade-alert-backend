import requests
import os
from dotenv import load_dotenv

load_dotenv()
FIREBASE_SERVER_KEY = os.getenv("FIREBASE_SERVER_KEY")

def send_push_notification(stock_list):
    url = "https://fcm.googleapis.com/fcm/send"
    headers = {
        "Authorization": f"key={FIREBASE_SERVER_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "to": "/topics/tradealerts",
        "notification": {
            "title": "Top 1-Day Trade Picks",
            "body": ", ".join([f"{s['symbol']} ({s['change']}%)" for s in stock_list])
        }
    }

    res = requests.post(url, json=body, headers=headers)
    print(f"Notification status: {res.status_code}")
