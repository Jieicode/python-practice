import requests
import csv
import time
from datetime import datetime
import os
import matplotlib.pyplot as plt


# ===== FXデータ取得 =====
def get_fx_data():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        usd_jpy = data["rates"]["JPY"]
        eur_jpy = usd_jpy / data["rates"]["EUR"]
        return usd_jpy, eur_jpy
    except Exception as e:
        print("FXデータ取得エラー:", e)
        return None, None


# ===== CSV保存 =====
def save_to_csv(usd_jpy, eur_jpy, change, signal):
    file_exists = os.path.exists("fx_data.csv")
    with open("fx_data.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["time", "USDJPY", "EURJPY", "change", "signal"])
        writer.writerow([
            str(datetime.now()),
            usd_jpy,
            eur_jpy,
            round(change, 2) if change is not None else 0,
            signal
        ])


# ===== シグナルログ =====
def save_signal_log(usd_jpy, eur_jpy, signal):
    with open("signal_log.txt", "a", encoding="utf-8") as f:
        f.write(
            f"{datetime.now()} | USDJPY:{round(usd_jpy,2)} "
            f"EURJPY:{round(eur_jpy,2)} SIGNAL:{signal}\n"
        )


# ===== CSV読み込み =====
def load_csv_data():
    prices = []
    if os.path.exists("fx_data.csv"):
        with open("fx_data.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                try:
                    prices.append(float(row[1]))
                except:
                    continue
    return prices


# ===== シグナル生成 =====
def generate_signal(prices):
    short_w = 3
    long_w = 5

    if len(prices) < long_w:
        return "NO_DATA", 0, 0, 0

    short_ma = sum(prices[-short_w:]) / short_w
    long_ma = sum(prices[-long_w:]) / long_w
    diff = short_ma - long_ma

    if diff > 0.01:
        signal = "BUY"
    elif diff < -0.01:
        signal = "SELL"
    else:
        signal = "NO_SIGNAL"

    return signal, short_ma, long_ma, diff


# ===== グラフ初期化 =====
plt.ion()
fig, ax = plt.subplots()


# ===== メイン =====
previous_usd = None
previous_signal = None

while True:
    usd_jpy, eur_jpy = get_fx_data()

    if usd_jpy is None:
        time.sleep(5)
        continue

    change = None
    if previous_usd is not None:
        change = usd_jpy - previous_usd

    prices = load_csv_data()
    signal, short_ma, long_ma, diff = generate_signal(prices)

    if change == 0 and signal == "NO_SIGNAL":
        print("変化なしスキップ")
        time.sleep(3)
        continue

    print("-----")
    print("時刻:", datetime.now())
    print("USDJPY:", round(usd_jpy, 2))
    if change is not None:
        print("差分:", round(change, 2))
    print("短期MA:", round(short_ma, 2))
    print("長期MA:", round(long_ma, 2))
    print("シグナル:", signal)

    if signal != previous_signal:
        if signal == "BUY":
            print("■■ BUY ■■")
        elif signal == "SELL":
            print("■■ SELL ■■")

        if signal in ["BUY", "SELL"]:
            save_signal_log(usd_jpy, eur_jpy, signal)

    save_to_csv(usd_jpy, eur_jpy, change, signal)

    previous_signal = signal
    previous_usd = usd_jpy

    # ===== リアルタイムグラフ =====
    prices = load_csv_data()

    ax.clear()
    ax.plot(prices, label="USDJPY")

    if len(prices) >= 5:
        short_ma = sum(prices[-3:]) / 3
        long_ma = sum(prices[-5:]) / 5

        ax.axhline(y=short_ma, linestyle="--", label="short MA")
        ax.axhline(y=long_ma, linestyle="--", label="long MA")

    ax.legend()
    ax.set_title("USDJPY RealTime")
    ax.grid()

    plt.pause(0.1)

    time.sleep(3)