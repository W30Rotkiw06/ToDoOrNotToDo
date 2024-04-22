import getpass
from datetime import datetime

tooObviousPasswords = ["12345678", "qwerty", "abcdefgh", "password", "haslo123", ]

def enterMail(input_text="Enter your email: "): # checking if provided "mail" is mail
    while True:
        mail = input(input_text).lower()
        at = 0
        dot = 0
        for char in mail[3:]:
            if char == "@": at +=1
        for char in mail[-4:]:
            if char == ".": dot +=1
        if at == 1 and dot ==1: return mail
        else: print(f"Your mail is not correct!")

# checking if created password is long enough and checking if passwords provided are the same
def enterPassword(input_text="Please enter your password: " ,min_len=8, one_password=False):
    if one_password==False:
        print("To increase Your safety, password is hidden.")
        print(f"Your password must be at least {min_len} chars long")
    while True:
        print(input_text, end="")
        password = getpass.getpass("")
        print("*" * len(password))

        if password.lower() in tooObviousPasswords:
            print("Your password is too obvious to guess, be more creative :-)")
            continue
        if len(password) < min_len and one_password == True: 
            print("Your password is too short")
            continue
        elif one_password == False:
            password2 = getpass.getpass("Enter your password again: ")
            print("*" * len(password),)
        
            if password != password2: print("Passwords aren't the same")
            else:
                print("Done")
                return password
            
        else: return password

def checkChoice(max=0): # checking if user gave int and is it in <0, max>
    while True:
        try: x = int(input())
        except ValueError: print("It's not a number")
        else: 
            if x <= max and max != 0: return x
            elif max == 0: return x
            else: print("Not found")

def showData(data, user): # printing todo list in nice way
    i = 0
    index = []
    for todo in data:
        if todo["created_by"] != user: continue
        i += 1
        print("\n", i, end=".\t")
        for key, value in todo.items():
            if key == "created_at":
                value = datetime.fromisoformat(value).strftime("%d.%m, %H:%M")
            elif key == "id": index.append(value)  
            if value != user:
                print(f"{value}\t", end="")
    if i ==0: print("\n\n\tYour ToDo list is empty\n\t\t   :-(")
    return index
       