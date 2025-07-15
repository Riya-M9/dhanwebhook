from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

API_KEY = "1107106579"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzUzMTY1Mzk4LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNzEwNjU3OSJ9.LKiqf2ACBEqQyGKfD8lRDTiJHT4mSTHQdDEe0l2IauGdLvA5gTFjGhudD8FYyfs0VuRG0UbGuCARsyAd83cWmQ"

def place_order(signal):
    payload = {
        "securityId": "2885",  # Reliance NSE
        "exchangeSegment": "NSE_EQ",
        "transactionType": signal.upper(),
        "productType": "INTRADAY",
        "quantity": 1,
        "disclosedQuantity": 0,
        "orderValidity": "DAY",
        "afterMarketOrder": False
    }

    headers = {
        "access-token": ACCESS_TOKEN,
        "dhanClientId": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post("https://api.dhan.co/orders", json=payload, headers=headers)
    print(response.status_code, response.text)
    return response.json()

@app.route('/trade', methods=['POST'])
def trade():
    data = request.get_json(force=True)
    print("Webhook received:", data)

    signal = data.get("signal")
    if not signal:
        return {"error": "Missing signal"}, 400

    return place_order(signal)

@app.route('/')
def home():
    return "✅ Webhook is live."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

