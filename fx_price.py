import requests

url = "https://api.exchangerate-api.com/v4/latest/USD"

data = requests.get(url).json()

usd_jpy = data["rates"]["JPY"]

print("USDJPY:", usd_jpy)

