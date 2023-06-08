name = [""] * 3
total = [0] * 3
averageMark = [0] * 3
mark = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

for student in range(3):
    name[student] = input("Enter student name: ")
    for m in range(5):
        print("Enter mark", m+1, ": ")
        mark[student][m] = int(input())
        total[student] = total[student] + mark[student][m]

    passinggrade = int(input("What is a passing grade? "))

    print("Total for student", name[student], total[student])
    averageMark[student] = round(total[student] / 5, 1)
    print("Average mark for", name[student], averageMark[student])

    if total[student] >= passinggrade:
        print(name[student], "is passing!")
    else:
        print(name[student], "is failing!")

input("\nPress ENTER to exit program")
