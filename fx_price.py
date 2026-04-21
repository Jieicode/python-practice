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
            usd_jpy,
            eur_jpy,
            round(change, 2) if change is not None else 0,
            signal
        ])


def save_signal_log(usd_jpy, eur_jpy, signal):
    with open("signal_log.txt", "a", encoding="utf-8") as f:
        f.write(
            str(datetime.now()) +
            " USDJPY: " + str(round(usd_jpy, 2)) +
            " EURJPY: " + str(round(eur_jpy, 2)) +
            " SIGNAL: " + signal +
            "\n"
        )

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
    short_ma = 0
    long_ma = 0
    difference_ma = 0

    if len(usd_list) >= long_window:
        short_ma = sum(usd_list[-short_window:]) / short_window
        long_ma = sum(usd_list[-long_window:]) / long_window
        difference_ma = short_ma - long_ma

        if difference_ma > 0.01:
            signal = "BUY"
        elif difference_ma < -0.01:
            signal = "SELL"
        else:
            signal = "NO_SIGNAL"
    else:
        signal = "NO_DATA"

    return signal, short_ma, long_ma, difference_ma


previous_usd = None

while True:
    usd_jpy, eur_jpy = get_fx_data()
    print("USDJPY:", usd_jpy)

    usd_list = load_csv_data()
    calculate_stats(usd_list)

    change = None
    if previous_usd is not None:
        change = usd_jpy - previous_usd
        print("前回との差:", round(change, 2))

    signal, short_ma, long_ma, difference_ma = generate_signal(usd_list)

    if change == 0 and signal == "NO_SIGNAL":
        print("値が変わっていないためスキップ")
        time.sleep(60)
        continue

    print("短期平均:", round(short_ma, 2))
    print("長期平均:", round(long_ma, 2))
    print("移動平均の差:", round(difference_ma, 4))
    print("シグナル:", signal)

    if signal == "BUY":
        print("■■■ BUYシグナル発生 ■■■")
    elif signal == "SELL":
        print("■■■ SELLシグナル発生 ■■■")

    if signal == "BUY" or signal == "SELL":
        save_signal_log(usd_jpy, eur_jpy, signal)
        print("signal_log保存しました")

    save_to_csv(usd_jpy, eur_jpy, change, signal)

    print("時刻:", datetime.now())
    print("USDJPY:", round(usd_jpy, 2))
    print("EURJPY:", round(eur_jpy, 2))
    print("----------------------")

    previous_usd = usd_jpy
    time.sleep(60)

print("------ FX情報 ------")
print("時刻:", datetime.now())
print("USDJPY:", usd_jpy)
print("EURJPY:", eur_jpy)

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

