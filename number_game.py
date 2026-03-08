import random
answer = random.randint(1,10)
guess = int(input("1～10の数字を当ててください:"))
if guess == answer:
    print("正解！")
else:
    print("はずれ！　正解は", answer)