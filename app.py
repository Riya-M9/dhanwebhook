from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)

API_KEY = "1107106579"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQ5MDMwNzc0LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNzEwNjU3OSJ9.JjwLsVu3jr_s1vi-JQTYVbP1ojgbY1nGvZasG8qkmmRnT8aLny-EBc7iyaOCK5N1cTIeMzDFk4pRdgnc29-3iA"

def place_order(signal, symbol, quantity):
    # Validate inputs
    if not signal or not symbol or quantity is None:
        print("❌ Invalid inputs:", signal, symbol, quantity)
        return {"error": "Missing or invalid mandatory fields"}

    try:
        quantity = int(quantity)
        if quantity <= 0:
            print("❌ Quantity must be positive:", quantity)
            return {"error": "Quantity must be a positive integer"}
    except Exception as e:
        print("❌ Quantity must be an integer:", quantity, "Error:", e)
        return {"error": "Quantity must be an integer"}

    payload = {
        "transactionType": signal.upper(),
        "securityId": symbol.upper(),
        "quantity": quantity,
        "orderType": "MARKET",
        "productType": "INTRADAY",
        "exchangeSegment": "NSE_EQ",
        "validity": "DAY"
    }

    print("📤 Payload to Dhan API:", payload)

    headers = {
        "access-token": ACCESS_TOKEN,
        "dhan-client-id": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://api.dhan.co/orders", headers=headers, json=payload)
        print("📥 Response status:", response.status_code)
        print("📥 Response text:", response.text)
        return response.json()
    except Exception as e:
        print("❌ Exception during order placement:", e)
        return {"error": "Exception during API call"}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("🔔 Incoming webhook data:", data)

    if not data:
        print("❌ No JSON data received")
        return jsonify({"error": "No JSON data received"}), 400

    try:
        signal = data["transactionType"]
        symbol = data["securityId"]
        quantity = data["quantity"]
    except KeyError as e:
        print(f"❌ Missing field in webhook data: {e}")
        return jsonify({"error": f"Missing field {e}"}), 400

    return place_order(signal, symbol, quantity)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
