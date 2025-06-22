from flask import Flask, request
import requests
import json

app = Flask(__name__)

API_KEY = "1107106579"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzUxMjAzNzA0LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNzEwNjU3OSJ9.pjSb8r0qWYvGJ7lOlLiYtDn7X_iDsdwsa5Eycq0gl8LsSBapC2vC-Kl45KNoxHO5mjf4VgUA0zfYKwltpzNeIA"

def place_order(signal, ticker, price):
    dhan_url = "https://api.dhan.co/orders"

    payload = {
        "exchangeSegment": "NSE_EQ",                # Required!
        "transactionType": "BUY" if signal.upper() == "BUY" else "SELL",
        "symbol": ticker,
        "quantity": 1,
        "orderType": "MARKET",
        "productType": "INTRADAY"                   # Also should be 'productType' not 'product'
    }

    headers = {
        "access-token": ACCESS_TOKEN,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Dhan-Client-Id": API_KEY
    }

    print("📤 Sending payload to Dhan:", json.dumps(payload, indent=2))
    response = requests.post(dhan_url, json=payload, headers=headers)
    print("📥 Dhan response:", response.text)
    return response.json()


@app.route('/trade', methods=['POST'])
def trade():
    data = request.json
    print("🚨 Webhook triggered. Incoming data:", data)

    signal = data.get('signal')
    ticker = data.get('ticker')
    price = data.get('price')

    if not all([signal, ticker, price]):
        return {"error": "Missing signal, ticker, or price"}, 400

    return place_order(signal, ticker, price)

@app.route('/')
def home():
    return "✅ Webhook server is live."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
