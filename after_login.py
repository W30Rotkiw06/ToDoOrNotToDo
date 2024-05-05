from tkinter import *
from supabase import create_client
from datetime import datetime, timezone
import pytz

def main_window(session, supabase):
    def onClick():
        window.destroy()
        session = supabase.auth.sign_out()

    def formatDate(date): # Formating date from iso to  DD:MM @ HH:MM in local timezone
        utc_date = datetime.fromisoformat(date).replace(tzinfo=pytz.utc) 
        return utc_date.astimezone(datetime.now(timezone.utc).astimezone().tzinfo).strftime("%d.%m @ %H:%M")




    def showData(window, data, user, show_done=True): # printing todo list in nice way
        column, row = 0, 0
        tab = Label(tab_frame, text="NR").grid(row=row, column=0, sticky="nsew")
        tab = Label(tab_frame, text="DATE").grid(row=row, column=1, sticky="nsew")
        tab = Label(tab_frame, text="NAME").grid(row=row, column=2, sticky="nsew")

        for todo in data:
            column = 0
            if todo["created_by"] != user: continue
            if show_done == False:
                if todo["is_done"] == True: continue
            row += 1

            tab = Label(tab_frame, text=f"{row}.")
            tab.grid(row=row, column=column, sticky="nsew")
            column += 1
            for key, value in todo.items():
                if key == "id" or key == "is_done" or key == "created_by": continue
                elif key == "created_at": 
                    try: value = formatDate(value)
                    except: value = "XX:XX @ XX:XX"
                elif key == "is_done":
                    value = bool(value)
                    if value == True: value = "✅"
                    else: value = "❌"
                tab = Label(tab_frame, text=value)
                tab.grid(row=row, column=column, sticky="n")
                column += 1

        if row == 0: 
            text_lbl = Label(window, text="Your ToDo list is empty")
            text_lbl.pack()

    

    window = Tk(className="ToDo || !ToDO")
    window.geometry("800x600")
    user_lbl = Label(window, text=f"Hello, {session.user.email}")
    user_lbl.pack()

    tab_frame = Frame(window)
    tab_frame.pack(fill=X)



    todos = supabase.table("todos").select("id, is_done, created_at, name, created_by").execute()
    showData(window, todos.data, session.user.email)
    

    window.mainloop()

if __name__ == "__main__":
    print("Open main.py file")