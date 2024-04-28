# Impotring libaries

import os
from supabase import create_client
from gotrue.errors import AuthError

from functions import enterMail, enterPassword, checkChoice, showData
from time import sleep
from sys import platform


# Supabase configuration
url = "https://pymxbbtuleqllrnvxvqe.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB5bXhiYnR1bGVxbGxybnZ4dnFlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTMxOTk0MjMsImV4cCI6MjAyODc3NTQyM30.OJpVZzwzICyKN2Eq0S2AtXJAIGLGV3OAp8H_MnDgAtM"
supabase=create_client(url, key)


if platform == "darwin":
    command ="clear"
else:
    command ="cls"

session = None
os.system(command)

# Downloading mails of all users
users = supabase.table("list_of_users").select("user").execute()
list_of_users = []
for user in users.data: list_of_users.append(user["user"])

# Logging in or creating new user
while session == None: 
    email = enterMail()    

    if email in list_of_users: 
        password = enterPassword(one_password=True)

        try: session = supabase.auth.sign_in_with_password({ "email": email, "password": password})
        except AuthError:
            print("Your password or mail is incorrect")
        else: print("Logged succesfully")

    else:
        print("You need to create new account\n")
        password = enterPassword()
        session = supabase.auth.sign_up({ "email": email, "password": password})
        print("Succesfully created new account")
        supabase.table("list_of_users").insert({"user": email}).execute()


while True:
    user = session.user.email

    # cleaning screan and displaying user
    sleep(0.5)
    os.system(command)
    print(f"User: {user}\n")


    # printing todo list
    todos = supabase.table("todos").select("id, created_at, name, created_by").execute()
    print("\nNR\tKEY\tDATE\t\tNAME\t", end="")
    indexes = showData(todos.data, user)

        
    # choice of actions
    options = 1
    print("\n\nWhat do you want to do? Type:")
    print("1 - Add new ToDo")
    if len(indexes) >0:
        print("2 - Delete ToDo")
        options += 1
    print("0 - Log out")

    choice = checkChoice(options)

    # Inserting new ToDo
    if choice == 1:
        new_todo = input("\nEnter your ToDo:\n").capitalize()
        todos = supabase.table("todos").insert({"name":new_todo, "created_by" : user}).execute()
    
    # Deleting ToDo
    elif choice == 2:
        print("\nType key of ToDo that you want to delete: ", end="")
        del_choice = checkChoice()
        if del_choice in indexes:
            todos = supabase.table("todos").delete().eq("id", del_choice).execute()
            print("Deleted succesfully")
        else: print("Error, key not found")
        sleep(0.4)

    else: break

os.system(command)
print("Logging out", end="")
for i in range(3):
    sleep(0.3)
    print(".", end="")

session = supabase.auth.sign_out()