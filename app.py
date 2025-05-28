from flask import Flask, request
import requests

app = Flask(__name__)

API_KEY = "1107106579"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQ5MDMwNzc0LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNzEwNjU3OSJ9.JjwLsVu3jr_s1vi-JQTYVbP1ojgbY1nGvZasG8qkmmRnT8aLny-EBc7iyaOCK5N1cTIeMzDFk4pRdgnc29-3iA"

def place_order(signal, ticker, price):
    dhan_url = "https://api.dhan.co/orders"
    payload = {
        "transaction_type": "BUY" if signal.upper() == "BUY" else "SELL",
        "symbol": ticker,
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
    return requests.post(dhan_url, json=payload, headers=headers).json()

@app.route('/trade', methods=['POST'])
def trade():
    data = request.json
    signal = data.get('signal')
    ticker = data.get('ticker')
    price = data.get('price')
    return place_order(signal, ticker, price)

if __name__ == '__main__':
    app.run()