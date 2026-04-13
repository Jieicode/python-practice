usd_list = []
import requests
import csv
import matplotlib.pyplot as plt
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

import os

if not os.path.exists("fx_data.csv"):
    with open("fx_data.csv","w",newline="",encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["time","USDJPY","EURJPY","change"])

previous_usd = None

try:
    with open("fx_data.csv","r",encoding="utf-8") as f:
        rows = list(csv.reader(f))
        if len(rows) > 0:
            previous_usd = float(rows[-1][1])
except:
    previous_usd = None

if previous_usd:
    change = usd_jpy - previous_usd
    print("前回との差:", round(change,2))

    if abs(change) > 0.3:
        print("大きく動きました")

usd_list = []

with open("fx_data.csv","r",encoding="utf-8") as f:
    rows = list(csv.reader(f))

    for row in rows[1:]:
        usd_list.append(float(row[1]))

if len(usd_list) > 0:

    print("データ数:", len(usd_list))

    avg = sum(usd_list) / len(usd_list)
    print("平均USDJPY:", round(avg,2))

    max_price = max(usd_list)
    min_price = min(usd_list)

    print("最高USDJPY:", round(max_price,2))
    print("最安USDJPY:", round(min_price,2))

    if usd_jpy > avg:
        print("平均より高い")
    else:
        print("平均より低い")

        plt.plot(usd_list)
        plt.title("USDJPY price history")
        plt.xlabel("data count")
        plt.ylabel("price")
        plt.show()

with open("fx_data.csv", "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
    str(datetime.now()),
    round(usd_jpy,2),
    round(eur_jpy,2),
    round(change,2) if previous_usd else 0
])
    
if usd_jpy > 150:
    print("USDJPYは高め")
else:
    print("USDJPYは低め")

with open("fx_data.txt","a") as f:
    f.write(str(datetime.now()) + 
        " USDJPY: " + str(round(usd_jpy,2)) + 
        " EURJPY: " + str(round(eur_jpy,2)) + 
        "\n")
    
print("ここまで動いている")
