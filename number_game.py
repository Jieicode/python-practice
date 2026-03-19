import random

print("難易度選んでください")
print("1 : 1-10")
print("2 : 1-50")
print("3 : 1-100")

level = input("選択 : ")

if level == "1":
    max_number = 10
    max_attempts = 3
elif level == "2":
    max_number = 50
    max_attempts = 5
else:
    max_number = 100
    max_attempts = 7

play = "y"

while play == "y":
    answer = random.randint(1, max_number)
    count = 0

    while count < max_attempts:
        guess = int(input(f"1-{max_number}の数字を当ててください: "))
        count = count + 1

        if guess == answer:
            print("正解！", count, "回で当てました！")
            break
        elif guess > answer:
            print("もっと小さい(あと", max_attempts - count, "回)")
        else:
            print("もっと大きい(あと", max_attempts - count, "回)")

        if count == max_attempts and guess != answer:
            print("ゲームオーバー 正解は", answer)
            break

    play = input("もう一回遊びますか? y/n: ")