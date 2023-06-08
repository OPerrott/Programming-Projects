import random

number = random.randint(1, 100)
tries = 10

while tries > 0:
    guess = int(input("What is your guess? "))

    if guess > number:
        print("The number is smaller than", guess)
    elif number > guess:
        print("The number is bigger than", guess)
    else:
        print("Well done! You are correct")
        tries = tries - 10

    tries = tries - 1
