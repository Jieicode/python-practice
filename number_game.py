import random
answer = random.randint(1,10)
count = 0
while count < 5:
    guess = int(input("1～10の数字を当ててください:"))
    count = count + 1
    if guess == answer:
        print("正解！")
        break
    elif guess > answer:
        print("もっと小さい")
    else:
        print("もっと大きい")
if count == 5 and guess != answer:
    print("ゲームオーバー　正解は", answer)