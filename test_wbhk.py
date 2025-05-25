import requests

data = {
    "transactionType": "BUY",
    "securityId": "RELIANCE",
    "quantity": 1
}

res = requests.post("https://your-render-app.onrender.com/webhook", json=data)
print(res.status_code)
print(res.text)
