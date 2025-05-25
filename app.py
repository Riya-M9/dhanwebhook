from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Dhan API credentials
API_KEY = "1107106579"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQ3OTk0ODI5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNzEwNjU3OSJ9.tI_gnikieURrD4egCqCjftjFrELDWbTh0HWcv-NtHdqxWzpcJfRqo-BdYrQ_XeyhWKZ351qMiFNX_4qkltOoJQ"

def place_order(signal, symbol, quantity=1):
    url = "https://api.dhan.co/orders"
    headers = {
        "access-token": ACCESS_TOKEN,
        "dhan-client-id": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "transactionType": "BUY" if signal.upper() == "BUY" else "SELL",
        "security_id": symbol,
        "quantity": quantity,
        "order_type": "MARKET",
        "product_type": "INTRADAY",
        "exchangeSegment": "NSE_EQ",
        "validity": "DAY"
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    # Ensure correct keys from TradingView
    signal = data.get("transaction_type")
    symbol = data.get("symbol")
    quantity = data.get("quantity", 1)

    result = place_order(signal, symbol, quantity)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
