import random
play = "y"
while play =="y":
    answer = random.randint(1,10)
    count = 0
    while count < 5:
       guess = int(input("1～10の数字を当ててください:"))
       count = count + 1
       if guess == answer:
           print("正解！", count, "回で当てました！")
           break
       elif guess > answer:
           print("もっと小さい(あと", 5-count, "回)")
       else:
           print("もっと大きい(あと", 5-count, "回)")
if count == 5 and guess != answer:
    print("ゲームオーバー　正解は", answer)

play = input("もう一回遊びますか? y/n: ")