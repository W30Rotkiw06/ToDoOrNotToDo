# Importing libaries
from tkinter import *
from functions import doWeHaveInternet, config
from gotrue.errors import AuthError
from after_login import main_window
import os

# I hate tkinter

# Creating login window
def createWindow():


    
    def input_mail():

        # Checking if given password is correct and opening main window
        def check_password():
            def destroyWin():
                window.withdraw()
                main_window(session)

            
                


            session = None
            password = pass1_ent.get()
            if mail not in list_of_users and len(password) < 8:
                if len(password) < 8: 
                    enter_mail_lbl.config(text="Your password is too short", foreground="red")
                    pass1_ent.delete(0,END)

                else: # Creating new account
                    enter_mail_lbl.config(text="Signed up succesfuly", foreground="green")
                    session = supabase.auth.sign_up({ "email": mail, "password": password})
                    supabase.table("list_of_users").insert({"user": mail}).execute()
                    

                    window.after(100, destroyWin)

            else: #Logging into existing account
                try:
                    session = supabase.auth.sign_in_with_password({ "email": mail, "password": password})
                except AuthError: 
                    enter_mail_lbl.config(text="Your password is incorrect", foreground="red")
                    pass1_ent.delete(0,END)
                else:
                    enter_mail_lbl.config(text="Logged succesfuly", foreground="green")
                    

                    window.after(100, destroyWin)

        mail = mail_ent.get().lower()
        at = 0
        dot = 0
        for char in mail[3:]:
            if char == "@": at +=1
        for char in mail[-4:-1]:
            if char == ".": dot +=1
        if at == 1 and dot ==1:
            

            enter_mail_lbl.config(text="Good, now enter your password", foreground="green")
            pass1_ent = Entry(frame, show="*")
            pass1_ent.pack()
            

            os.system("clear")
            button.destroy()
            

            mail_ent.destroy()
            button_pass = Button(frame, text="Sign In", background="blue", command=check_password)
            button_pass.pack()
            print("check")

            if mail not in list_of_users: 
                button_pass.config(text="Sign Up")
                enter_mail_lbl.config(text="You will need to create new account")

        else: 
            enter_mail_lbl.config(text="It's not a mail",foreground="red")
            mail_ent.delete(0,END)

    
    # Creating window
    window = Tk(className="Login | ToDo || !ToDO")
    frame = Frame(window).pack(fill=X)

    window.geometry("250x80")

    # Checking internet connection
    internet = doWeHaveInternet()
    if internet == False: 
        lbl = Label(text="You are offline")
        lbl.pack()
        window.after(5000, window.destroy)  # Close window after 5 seconds if offline
        window.mainloop()
        exit()

    # Configiurating supabase
    list_of_users = []
    supabase = config()
    users = supabase.table("list_of_users").select("user").execute()
    for user in users.data: list_of_users.append(user["user"])



    # Creating labels, entries and button
    mail_text = 'Enter your email:'
    enter_mail_lbl = Label(frame, text=mail_text)
    enter_mail_lbl.pack()

    mail_ent = Entry(frame)
    mail_ent.pack()

    button = Button(frame, text="Continue", background="blue", command=input_mail)
    button.pack()


    window.mainloop()



if __name__ == "__main__": createWindow()