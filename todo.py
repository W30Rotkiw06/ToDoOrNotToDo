# Impotring libaries
import os
from gotrue.errors import AuthError
from functions import doWeHaveInternet, config, enterMail, enterPassword, checkChoice, showData
from time import sleep
from sys import platform
from datetime import datetime, timezone

session, list_of_users, attempts, show_done = None, [], 0, True # Useful vars

# checking platform
command = "cls" if platform == "win32" else "clear"
os.system(command) # <-cleaning terminal

# Checking internet connection
internet = doWeHaveInternet()
if internet == False: 
    print("You are offline :=(")
    exit()

# Supabase configuration
supabase = config()

# Downloading mails of all users
users = supabase.table("list_of_users").select("user").execute()
for user in users.data: list_of_users.append(user["user"])

# Logging in or creating new user
email = enterMail()    
while session == None: 
    if email in list_of_users: 
        password = enterPassword(one_password=True)

        try: session = supabase.auth.sign_in_with_password({ "email": email, "password": password})
        except AuthError:
            attempts += 1
            print(f"Your password is incorrect, {3-attempts} attempts left")
        else: print("Logged succesfully")
        if attempts >= 3:
            print("Login failed")
            exit()
    else:
        print("You need to create new account\n")
        password = enterPassword()
        session = supabase.auth.sign_up({ "email": email, "password": password})
        print("Succesfully created new account")
        supabase.table("list_of_users").insert({"user": email}).execute()

user = session.user.email

while True:
    # cleaning screan and displaying user
    os.system(command)
    print(f"User: {user}\n")


    # printing todo list
    todos = supabase.table("todos").select("id, is_done, created_at, name, created_by").execute()
    print("\nNR\tKEY\tSTATUS\tDATE\t\tNAME", end="")
    indexes = showData(todos.data, user, show_done)

        
    # choice of actions
    options = 5 # n-1
    print("\n\nWhat do you want to do? Type:")
    print("1 - Add new ToDo")
    

    if len(indexes) >0:
        print("2 - Mark ToDO as done/undone")
        print("3 - Rename ToDo")
        print("4 - ", end='')
        print("Hide" ,end=' ') if show_done == True else print("Show", end=' ')
        print("ToDos marked as done")
        print("5 - Delete ToDo")
    else: options = 1
    print("0 - Log out")

    choice = checkChoice(options)

    # Inserting new ToDo
    if choice == 1:
        new_todo = input("\nEnter your ToDo:\n").capitalize()
        todos = supabase.table("todos").insert({"name":new_todo, "created_by" : user}).execute()
    
    # Marking ToDo as done
    elif choice == 2:
        print("\nType key of ToDo that you want to mark as done/undone: ", end="")
        mark_choice = checkChoice()
        if mark_choice in indexes:
            if supabase.table("todos").select("is_done").eq("id", mark_choice).execute().data[0]["is_done"] == False:
                todos = supabase.table("todos").update({"is_done": True}).eq("id", mark_choice).execute()
                print("Marked as done")
            else: 
                todos = supabase.table("todos").update({"is_done": False}).eq("id", mark_choice).execute()
                print("Marked as undone")
        else: print("Error, key not found")
        sleep(0.4)

    # Renaming ToDO
    elif choice == 3:
        print("\nType key of ToDo that you want to rename: ", end="")
        mark_choice = checkChoice()
        if mark_choice in indexes:
                todos = supabase.table("todos").update({"created_at": datetime.now(timezone.utc).isoformat(),"name": input("\nEnter your new ToDo:\n"), "is_done": False}).eq("id", mark_choice).execute()
                print("Renamed succesfuly")
                
        else: print("Error, key not found")
        sleep(0.4)

    elif choice == 4:
        if show_done == True: show_done = False
        else: show_done = True

    # Deleting ToDo2
    elif choice == 5:
        print("\nType key of ToDo that you want to delete: ", end="")
        del_choice = checkChoice()
        if del_choice in indexes:
            todos = supabase.table("todos").delete().eq("id", del_choice).execute()
            print("Deleted succesfully")
        else: print("Error, key not found")
        sleep(0.4)

    else:
        os.system(command)
        print("Logging out", end="")
        for i in range(3):
            sleep(0.3)
            print(".", end="")
        session = supabase.auth.sign_out()