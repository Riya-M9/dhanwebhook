from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# REPLACE with valid credentials
API_KEY = "1107106579"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQ5MDMwNzc0LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNzEwNjU3OSJ9.JjwLsVu3jr_s1vi-JQTYVbP1ojgbY1nGvZasG8qkmmRnT8aLny-EBc7iyaOCK5N1cTIeMzDFk4pRdgnc29-3iA"

def place_order(signal, symbol, quantity):
    url = "https://api.dhan.co/orders"

    headers = {
        "access-token": ACCESS_TOKEN,
        "dhan-client-id": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "transactionType": signal.upper(),
        "securityId": symbol.upper(),
        "quantity": quantity,
        "orderType": "MARKET",
        "productType": "INTRADAY",
        "exchangeSegment": "NSE_EQ",
        "validity": "DAY"
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    # Extract required fields
    try:
        signal = data["transactionType"]
        symbol = data["securityId"]
        quantity = data["quantity"]
    except KeyError as e:
        return jsonify({"error": f"Missing field {e}"}), 400

    return place_order(signal, symbol, quantity)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)