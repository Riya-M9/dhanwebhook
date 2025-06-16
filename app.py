from flask import Flask, request
import requests
import json

app = Flask(__name__)

API_KEY = "1107106579"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzUwNjcxOTc2LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNzEwNjU3OSJ9.-d4-g1HN2cjAybfcLo0ZVcSzW_5jnIogMiIKGsUZGG4fQAi0Z8iqvb85nkV_5v81FBM596c-LY0PBY1qMJ3Qhg"

DHAN_ORDER_URL = "https://api.dhan.co/orders"

def place_order(signal, ticker, price):
    transaction_type = "BUY" if signal.upper() == "BUY" else "SELL"

    payload = {
        "transaction_type": transaction_type,
        "symbol": "RELIANCE",  # Hardcoded
        "quantity": 1,
        "order_type": "MARKET",
        "product": "INTRADAY"
    }

    headers = {
        "access-token": ACCESS_TOKEN,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Dhan-Client-Id": API_KEY
    }

    response = requests.post(DHAN_ORDER_URL, json=payload, headers=headers)
    print("📤 Order Sent:", json.dumps(payload, indent=2))
    print("📥 Dhan Response:", response.json())
    return response.json()

@app.route('/trade', methods=['POST'])
def trade():
    data = request.json
    print("🚨 Webhook Received:", data)

    signal = data.get('signal')
    price = data.get('price')

    if not signal or not price:
        print("❌ Missing required data.")
        return {"error": "Missing data"}, 400

    return place_order(signal, "RELIANCE", price)

if __name__ == '__main__':
    app.run(debug=True)
