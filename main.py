from screener import fetch_candidates
from notifier import send_push_notification

def run_alert():
    print("Running screener...")
    top_stocks = fetch_candidates()
    if top_stocks:
        print("Top Stocks:", top_stocks)
        send_push_notification(top_stocks)
    else:
        print("No strong trades found.")

    run_alert()
