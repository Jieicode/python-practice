import requests
import csv
import matplotlib.pyplot as plt
from datetime import datetime
import os
import time


def get_fx_data():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    data = requests.get(url).json()

    usd_jpy = data["rates"]["JPY"]
    eur_jpy = usd_jpy / data["rates"]["EUR"]

    return usd_jpy, eur_jpy


def load_csv_data():
    usd_list = []

    if os.path.exists("fx_data.csv"):
        with open("fx_data.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)

            for row in reader:
                if len(row) < 2:
                    continue
                if row[1] == "USDJPY":
                    continue

                try:
                    usd_list.append(float(row[1]))
                except ValueError:
                    continue

    return usd_list


def save_to_csv(usd_jpy, eur_jpy, change, signal):
    if not os.path.exists("fx_data.csv"):
        with open("fx_data.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["time", "USDJPY", "EURJPY", "change", "signal"])

    with open("fx_data.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            str(datetime.now()),
            round(usd_jpy, 2),
            round(eur_jpy, 2),
            round(change, 2) if change is not None else 0,
            signal
        ])


usd_jpy, eur_jpy = get_fx_data()
usd_list = load_csv_data()

base_price = 150.00
difference = usd_jpy - base_price

if difference > 0:
    print("上昇:", round(difference, 2))
else:
    print("下降:", round(difference, 2))

print("取得時刻:", datetime.now())

previous_usd = None

try:
    if os.path.exists("fx_data.csv"):
        with open("fx_data.csv", "r", encoding="utf-8") as f:
            rows = list(csv.reader(f))
            if len(rows) > 1:
                previous_usd = float(rows[-1][1])
except:
    previous_usd = None

change = None
if previous_usd is not None:
    change = usd_jpy - previous_usd

    if abs(change) > 0.3:
        print("大きく動きました")


def calculate_stats(usd_list):
    generate_signal(usd_list)
    if len(usd_list) > 0:
        print("データ数:", len(usd_list))

        avg = sum(usd_list) / len(usd_list)
        print("平均USDJPY:", round(avg, 2))

        max_price = max(usd_list)
        min_price = min(usd_list)

        print("最高USDJPY:", round(max_price, 2))
        print("最安USDJPY:", round(min_price, 2))

def generate_signal(usd_list):
    short_window = 3
    long_window = 5
    signal = "NO_DATA"

    if len(usd_list) >= long_window:
        short_ma = sum(usd_list[-short_window:]) / short_window
        long_ma = sum(usd_list[-long_window:]) / long_window

        print("短期平均:", round(short_ma, 2))
        print("長期平均:", round(long_ma, 2))

        if short_ma > long_ma:
            print("買いシグナル")
            signal = "BUY"
        else:
            print("売りシグナル")
            signal = "SELL"
    else:
        print("移動平均を出すにはデータが足りません")

    return signal

previous_usd = None

while True:
    usd_jpy, eur_jpy = get_fx_data()
    usd_list = load_csv_data()

    calculate_stats(usd_list)

    change = None
    if previous_usd is not None:
        change = usd_jpy - previous_usd
        print("前回との差:", round(change, 2))

    signal = generate_signal(usd_list)

    save_to_csv(usd_jpy, eur_jpy, change, signal)

    print("時刻:", datetime.now())
    print("USDJPY:", round(usd_jpy, 2))
    print("EURJPY:", round(eur_jpy, 2))
    print("シグナル:", signal)
    print("----------------------")

    previous_usd = usd_jpy

    time.sleep(60)

print("------ FX情報 ------")
print("時刻:", datetime.now())
print("USDJPY:", round(usd_jpy, 2))
print("EURJPY:", round(eur_jpy, 2))

if previous_usd:
    print("前回との差:", round(change, 2))

print("シグナル:", signal)
print("-------------------")

plt.plot(usd_list, label="USDJPY")
plt.axhline(y=avg, linestyle="--", label="平均")
plt.title("USDJPY price history")
plt.xlabel("data count")
plt.ylabel("price")
plt.legend()
plt.grid()


