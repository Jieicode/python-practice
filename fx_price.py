import requests
from datetime import datetime

url = "https://api.exchangerate-api.com/v4/latest/USD"

data = requests.get(url).json()

usd_jpy = data["rates"]["JPY"]
eur_jpy = usd_jpy / data["rates"]["EUR"]

base_price = 150.00
difference = usd_jpy - base_price

if difference > 0:
    print("上昇:", round(difference,2))
else:
    print("下降:", round(difference,2))

print("取得時刻:",datetime.now())
print("USDJPY:", round(usd_jpy,2))
print("EURJPY:", round(eur_jpy,2))

if usd_jpy > 150:
    print("USDJPYは高め")
else:
    print("USDJPYは低め")

with open("fx_data.txt","a") as f:
    f.write(str(datetime.now()) + 
        " USDJPY: " + str(round(usd_jpy,2)) + 
        " EURJPY: " + str(round(eur_jpy,2)) + 
        "\n")
    
