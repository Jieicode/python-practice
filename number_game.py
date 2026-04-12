#数字当てゲーム
#ランダムで数字を作る
#回数制限内に当てるゲーム

import random
def show_help():
    print("=== 遊び方 ===")
    print("難易度を選びます")
    print("数字を入力して当てます")
    print("大きいか小さいかヒントが出ます")
    print("回数制限があります")


def show_menu():
    #メニュー表示関数
　　print("=== Number Game ===")
    print("1. ゲームを始める")
    print("2. 遊び方を見る")
    print("3. 終了")

　　while True:
        choice = input("選択してください: ")
        if choice == "1" or choice == "2" or choice =="3":
            return choice
        else:
            print("1,2,3で選んでください")

def select_difficulty():
　　#難易度選択
    print("難易度選んでください")
    print("1 : 1-10")
    print("2 : 1-50")
    print("3 : 1-100")

    while True:

        level = input("選択 : ")

        if level == "1":
            max_number = 10
            max_attempts = 3
            return max_number, max_attempts

        elif level == "2":
            max_number = 50
            max_attempts = 5
            return max_number, max_attempts

        elif level == "3":
            max_number = 100
            max_attempts = 7
            return max_number, max_attempts

        else:
            print("1,2,3で選んでください")

def play_game(max_number, max_attempts):
　　#メインゲーム処理

    play = 0

        while count < max_attempts:

            while True:
                try:
                    guess = int(input(f"1-{max_number}の数字を当ててください: "))
                    break
                except:
                    print("数字を入れてください")
            if guess < 1 or guess > max_number:
                print("範囲内の数字を入れてください")
                continue

            count = count + 1

            if guess == answer:
                print("正解！", count, "回で当てました！")
                break

            elif guess > answer:
                print("もっと小さい(あと", max_attempts-count, "回)")

            else:
                print("もっと大きい(あと", max_attempts-count, "回)")

            if count == max_attempts and guess != answer:
                print("ゲームオーバー 正解は", answer)

        play = input("もう一回遊びますか？ y/n: ")


menu = show_menu()

if menu == "1":
    max_number, max_attempts = select_difficulty()

elif menu == "2":
    show_help()
    max_number, max_attempts = select_difficulty()

else:
    print("終了します")
    exit()


play_game(max_number, max_attempts)