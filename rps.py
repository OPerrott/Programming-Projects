import random

user_action = input("Rock Paper Scissors: ")
possible_acition = ["Rock", "Paper", "Scissors"]
computer_action = random.choice(possible_acition)

if user_action == computer_action:
    print("It's a tie")
elif user_action == "Rock":
    if computer_action == "Scissors":
        print("Rock crushes scissors. You WIN")
    else:
        print("Paper covers rock. You LOSE")
elif user_action == "Paper":
    if computer_action == "Rock":
        print("Paper covers rock. You WIN")
    else:
        print("Scissors cuts paper. You LOSE")
elif user_action == "Scissors":
    if computer_action == "Paper":
        print("Scissors cuts paper. You WIN")
    else:
        print("Rock smashes scissors. You LOSE")
