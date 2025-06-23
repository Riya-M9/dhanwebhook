from flask import Flask, request
import requests
import json
from datetime import datetime

app = Flask(__name__)

API_KEY = "1107106579"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzUxMjAzNzA0LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNzEwNjU3OSJ9.pjSb8r0qWYvGJ7lOlLiYtDn7X_iDsdwsa5Eycq0gl8LsSBapC2vC-Kl45KNoxHO5mjf4VgUA0zfYKwltpzNeIA"

def place_order(signal, ticker, price):
    dhan_url = "https://api.dhan.co/orders"

    payload = {
        "exchangeSegment": "NSE_EQ",
        "transactionType": "BUY" if signal.upper() == "BUY" else "SELL",
        "productType": "INTRADAY",
        "orderType": "MARKET",
        "price": 0,
        "quantity": 1,
        "disclosedQuantity": 0,
        "symbol": "RELIANCE",
        "securityId": "INE002A01018",
        "orderValidity": "DAY",
    }

    headers = {
        "access-token": ACCESS_TOKEN,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Dhan-Client-Id": API_KEY
    }

    print("📤 Final Payload to Dhan:\n", json.dumps(payload, indent=2))
    res = requests.post(dhan_url, json=payload, headers=headers)
    print("📥 Dhan Response:", res.text)
    return res.json()


@app.route('/trade', methods=['POST'])
def trade():
    try:
        print("===================================")
        print("🚨 Webhook HIT at:", datetime.now())
        print("🚨 Raw Payload:", request.get_json())
        print("===================================")

        data = request.get_json()
        signal = data.get('signal')
        ticker = data.get('ticker')
        price = data.get('price')

        if not all([signal, ticker, price]):
            print("❌ Missing fields in data")
            return {"error": "Missing signal, ticker or price"}, 400

        return place_order(signal, ticker, price)

    except Exception as e:
        print("❌ Exception in /trade:", str(e))
        return {"error": "Internal error"}, 500

@app.route('/')
def home():
    return "✅ Webhook server is live."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
