import requests

data = {
    "transactionType": "BUY",
    "securityId": "RELIANCE",
    "quantity": 1
}

res = requests.post("https://dhanwebhook.onrender.com/webhook", json=data)
print(res.status_code)
print(res.text)
