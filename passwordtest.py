upper_flag = False
lower_flag = False
num_flag = False


# program asks the user to enter a password
# program measure the length of the inputted password
password = input("Input a password: ")
passwordlength = len(password)


#while the length is shorter than 6 or longer than 12 characters
#The program asks to enter again through a while loop 
while (passwordlength < 6) or (passwordlength > 12):
  password = input("Please enter a password: ")
  passwordlength = len(password)


#The string is checked if it contains uppercase letters
for x in range(passwordlength):
  uppercasecheck = password[x].isupper()
  if uppercasecheck == True:
    upper_flag = True


#if it includeds uppercase letters, the following is printed
print("Uppercase characters in my password is", upper_flag)


#the string is check for lowercase letters
for x in range(passwordlength):
  lowercasecheck = password[x].islower()
  if lowercasecheck == True:
    lower_flag = True

#if it contains lowercase the following is printed
print("Lowercase characters in my password is", lower_flag)


#the string is checked if it contains numbers
for x in range(passwordlength):
  numcasecheck = password[x].isdigit()
  if numcasecheck == True:
    num_flag = True

#if it contains numbers then the following is printed 
print("Number of characters in my password is", num_flag)

#if all 3 criterias are met, the password is strong
if num_flag and lower_flag and upper_flag is True:
  print("Your password is strong.")
  
#if only 2 criterias are met, the password is medium
elif num_flag and lower_flag or num_flag and upper_flag or lower_flag and upper_flag is True:
  print("Your password is medium")
  
#if only one criteria is met, the password is weak
elif num_flag or upper_flag or lower_flag is True:
  print("Your password is weak")