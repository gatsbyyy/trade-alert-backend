import requests
import os
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def fetch_candidates():
    symbols = ["MARA", "SOFI", "PLTR", "IDEX", "SNDL", "TQQQ", "BBIG", "AMC", "NIO", "RIVN"]
    results = []

    for symbol in symbols:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
        res = requests.get(url).json()
        current = res.get("c")
        open_price = res.get("o")

        if not current or not open_price:
            continue

        price_change = (current - open_price) / open_price * 100
        if 1 <= current <= 30 and price_change > 1.5:
            results.append({
                "symbol": symbol,
                "price": current,
                "change": round(price_change, 2)
            })

    results.sort(key=lambda x: x["change"], reverse=True)
    return results[:5]
