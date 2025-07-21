from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

API_KEY = "1107106579"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzUzMTY1Mzk4LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNzEwNjU3OSJ9.LKiqf2ACBEqQyGKfD8lRDTiJHT4mSTHQdDEe0l2IauGdLvA5gTFjGhudD8FYyfs0VuRG0UbGuCARsyAd83cWmQ"
# VI (Vodafone Idea) NSE security ID (from instrument list)
VI_SECURITY_ID = "1594"  # Confirm from the latest NSE_EQ instrument file

def place_order(signal):
    payload = {
        "dhanClientId": API_KEY,
        "securityId": VI_SECURITY_ID,
        "exchangeSegment": "NSE_EQ",
        "transactionType": signal.upper(),  # BUY or SELL
        "productType": "INTRADAY",
        "orderType": "MARKET",
        "validity": "DAY",
        "quantity": 1,
        "disclosedQuantity": 0,
        "afterMarketOrder": False
    }

    headers = {
        "access-token": ACCESS_TOKEN,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post("https://api.dhan.co/orders", json=payload, headers=headers)
    print(f"Status: {response.status_code}, Response: {response.text}")
    return response.json()

@app.route('/trade', methods=['POST'])
def trade():
    try:
        data = request.get_json(force=True)
        print("Received webhook:", data)

        signal = data.get("signal")
        ticker = data.get("ticker")

        if not signal or not ticker:
            return {"error": "Missing 'signal' or 'ticker'"}, 400

        if ticker.upper() != "VI":
            return {"error": f"Only VI symbol allowed. Received: {ticker}"}, 403

        return place_order(signal)

    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/')
def home():
    return "✅ Webhook listener is running for VI."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    