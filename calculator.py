num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))
operator = input("Enter an operator (* / + - %): ")

def multiplication():
    total = num1 * num2
    print(total)


def divide():
    total = num1 / num2
    print(total)


def add():
    total = num1 + num2
    print(total)


def sub():
    total = num1 - num2
    print(total)

if operator == "*":
    multiplication()
elif operator == "/":
    divide()
elif operator == "+":
    add()
elif operator == "-":
    sub()
