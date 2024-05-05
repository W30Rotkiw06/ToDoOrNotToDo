from tkinter import *

def main_window(session):
    def onClick():
        window.destroy()
        
    window = Tk(className="ToDo || !ToDO")
    user_lbl = Label(window, text=f"Hello, {session.user.email}")
    user_lbl.pack()
    

    button = Button(window, text="Continue", background="blue", command=onClick)
    button.pack()


    window.mainloop()
if __name__ == "__main__":
    print("Open main.py file")