from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace these with your actual Dhan API keys
API_KEY = "1107106579"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQ3OTk0ODI5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNzEwNjU3OSJ9.tI_gnikieURrD4egCqCjftjFrELDWbTh0HWcv-NtHdqxWzpcJfRqo-BdYrQ_XeyhWKZ351qMiFNX_4qkltOoJQ"

def place_order(signal, symbol, quantity=1):
    url = "https://api.dhan.co/orders"
    headers = {
        "access-token": ACCESS_TOKEN,
        "Dhan-Client-Id": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "transaction_type": "BUY" if signal.upper() == "BUY" else "SELL",
        "security_id": symbol,
        "quantity": quantity,
        "order_type": "MARKET",
        "product_type": "INTRADAY",
        "exchange_segment": "NSE_EQ",
        "validity": "DAY"
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    symbol = data.get("symbol")
    signal = data.get("side")
    qty = data.get("qty", 1)
    result = place_order(signal, symbol, qty)
    return jsonify(result)

if __name__ == '__main__':
    app.run()
