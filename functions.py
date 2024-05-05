# Impotring libaries
import getpass
from datetime import datetime, timezone, timedelta
from supabase import create_client
import requests
import pytz


tooObviousPasswords = ["12345678", "qwerty", "abcdefgh", "password", "haslo123", ]
user_timezone = datetime.now(timezone.utc).astimezone().tzinfo # Download local timezone

def doWeHaveInternet(): # Checking if user has internet connection
    try:
        requests.get("https://google.com", timeout=5)
    except requests.ConnectionError: return False
    else: return True

def config(): # Supabase configuration
    url = "https://pymxbbtuleqllrnvxvqe.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB5bXhiYnR1bGVxbGxybnZ4dnFlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTMxOTk0MjMsImV4cCI6MjAyODc3NTQyM30.OJpVZzwzICyKN2Eq0S2AtXJAIGLGV3OAp8H_MnDgAtM"
    return create_client(url, key)


def enterMail(input_text="Enter your email: "): # checking if provided "mail" is mail
    while True:
        mail = input(input_text).lower().strip()
        at = 0
        dot = 0
        for char in mail[3:]:
            if char == "@": at +=1
        for char in mail[-4:]:
            if char == ".": dot +=1
        if at == 1 and dot ==1: return mail
        else: print(f"Your mail is  incorrect!")

# checking if created password is long enough and checking if passwords provided are the same
def enterPassword(input_text="Please enter your password: " ,min_len=8, one_password=False):
    if one_password==False:
        print(f"To increase Your safety, password is hidden. Password must be at least {min_len} chars long")
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

def formatDate(date): # Formating date from iso to  DD:MM @ HH:MM in local timezone
    utc_date = datetime.fromisoformat(date).replace(tzinfo=pytz.utc) 
    return utc_date.astimezone(user_timezone).strftime("%d.%m @ %H:%M")


def showData(data, user, show_done=True): # printing todo list in nice way
    i,index = 0, []
    for todo in data:
        if todo["created_by"] != user: continue
        if show_done == False:
            if todo["is_done"] == True: continue
        i += 1
        print("\n", i, end=".\t")
        for key, value in todo.items():
            if key == "created_at": 
                try: value = formatDate(value)
                except: value = "XX:XX @ XX:XX"
            elif key == "id": index.append(value)  
            if key == "is_done":
                value = bool(value)
                if value == True: value = "✅"
                else: value = "❌"
            if value != user: print(f"{value}\t", end="")
    if i ==0: print("\n\n\tYour ToDo list is empty\n\t\t   :-(")
    return index
       