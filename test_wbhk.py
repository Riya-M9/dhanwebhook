import requests

data = {
    "symbol": "RELIANCE",
    "transactionType": "BUY",         # renamed from "side"
    "quantity": 1,
    "order_type": "MARKET",
    "product_type": "INTRADAY",
    "exchangeSegment": "NSE_EQ",
    "validity": "DAY"
}

res = requests.post("https://dhanwebhook.onrender.com/webhook", json=data)
print(res.status_code)
print(res.text)
