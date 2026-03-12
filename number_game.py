import random
answer = random.randint(1,10)
guess = int(input("1～10の数字を当ててください:"))
if guess == answer:
    print("正解！")
elif guess > answer:
    print("もっと小さい")
else:
    print("もっと大きい")