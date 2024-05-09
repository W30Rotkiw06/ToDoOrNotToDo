from tkinter import *
from datetime import datetime, timezone
import pytz

from functions import config

def main_window(session, supabase):


    def formatDate(date): # Formating date from iso to  DD:MM @ HH:MM in local timezone
        utc_date = datetime.fromisoformat(date).replace(tzinfo=pytz.utc) 
        return utc_date.astimezone(datetime.now(timezone.utc).astimezone().tzinfo).strftime("%d.%m @ %H:%M")




    def showData(window, data, user, show_done=True): # printing todo list in nice way
        global rows, geometry
        column, row, rows = 0, 1, 0
        todo_names, todo_times, todo_boxes, values_boxes = [], [], [], []
        tab = Label(tab_frame, text="DONE").grid(row=row, column=0, sticky="nsew", )
        tab = Label(tab_frame, text="DATE").grid(row=row, column=1, sticky="nsew", )
        tab = Label(tab_frame, text="NAME").grid(row=row, column=2, sticky="nsew", )
        tab  = Label(tab_frame, text="SAVE").grid(row=row, column=3, sticky="nsew", )
        tab  = Label(tab_frame, text="").grid(row=row, column=4, sticky="nsew", )

        tab_frame.grid_columnconfigure(0, minsize=5)
        tab_frame.grid_columnconfigure(1, minsize=145)
        tab_frame.grid_columnconfigure(2, minsize=185)
        tab_frame.grid_columnconfigure(3, minsize=25)
        tab_frame.grid_columnconfigure(4, minsize=50)

        def accept(row, todo): # Saving changes in database
            if todo_names[row-2].get() == todo["name"]: return
            key = todo["id"]
            date_with_timezone = formatDate(datetime.now(timezone.utc).isoformat())
            
            todos = supabase.table("todos").update({"created_at" : datetime.now(timezone.utc).isoformat() ,"name": todo_names[row-2].get()}).eq("id", key)
            todo_times[row-2].config(text=date_with_timezone)
            todos.execute()

        def delete(row, todo):
            global rows, geometry
            key = todo["id"]
            # Delete row in table 
            for widget in tab_frame.grid_slaves():
                if int(widget.grid_info()["row"]) == row:
                    widget.grid_forget()
            rows -= 1
            if rows ==0: 
                empty_lbl = Label(bottom_frame, text="")
                empty_lbl.pack()
            else: 
                empty_lbl.destroy()

            geometry = f"450x{120 +(30)*rows}"
            window.geometry(geometry)

            # Delete in database
            todos = supabase.table("todos").delete().eq("id", key).execute()

        # Mark as done/undone in database
        def isDoneCheck(row, todo):
            key = todo["id"]
            updated_value = True if values_boxes[row-2].get() else False
            todos = supabase.table("todos").update({"is_done" :updated_value}).eq("id", key)
            todos.execute()
        
        def addNewToDo(row):
            todos = supabase.table("todos").insert({"created_at" : datetime.now(timezone.utc).isoformat(),"name":"", "created_by" : user}).execute()
            window.destroy()
            main_window(session, supabase)



        add_button = Button(bottom_frame, text="Add new todo", command= lambda row  =row:addNewToDo(row))
        add_button.pack()
        """log_out_button = Button"""
        
        for todo in data:
            

            column = 0
            if todo["created_by"] != user: continue
            if show_done == False:
                if todo["is_done"] == True: continue
            row += 1
            rows +=1
            for key, value in todo.items():
            
                if key == "id" or key == "created_by": continue
                elif key == "is_done":
                    values_boxes.append(BooleanVar())
                    values_boxes[row-2].set(bool(value))

                    todo_boxes.append(Checkbutton(tab_frame, offvalue=False, onvalue=True, variable=values_boxes[row-2], command= lambda row=row, todo=todo : isDoneCheck(row, todo)))
                    todo_boxes[row-2].grid(row=row, column=column)
                    if values_boxes[row-2].get() == True: todo_boxes[row-2].select()
                    else: todo_boxes[row-2].deselect()




                elif key == "created_at": 
                    try: value = formatDate(value)
                    except: value = "XX:XX @ XX:XX"
                    todo_times.append(Label(tab_frame, text=value))
                    todo_times[row-2].grid(row=row, column=column,)
                elif key != "name":
                    tab = Label(tab_frame, text=value)
                    tab.grid(row=row, column=column,)
                else: 
                    todo_names.append(Entry(tab_frame, border=1, width=30))
                    todo_names[row-2].insert(index=0, string=value)
                    todo_names[row-2].grid(row=row, column=column,)
                column += 1
            accept_button =  Button(tab_frame, text="✅", command= lambda row =row , todo= todo:  accept(row, todo))
            accept_button.grid(row=row, column=column)
            column += 1
            delete_button = Button(tab_frame, text="delete", background="red", foreground="white", command=lambda row=row , todo=todo: delete(row, todo))
            delete_button.grid(row=row, column=column)

        if rows == 0: 
            empty_lbl = Label(bottom_frame, text="")
            empty_lbl.pack()
        geometry = f"450x{120 +(30)*rows}"
        window.geometry(geometry)

    

    window = Tk(className="ToDo || !ToDO")
    geometry = f"450x120"
    window.geometry(geometry)
    window.resizable(False, False)

    user_lbl = Label(window, text=f"Hello, {session.user.email}", font="TimesNewRoman", )
    user_lbl.pack()

    tab_frame = Frame(window)
    tab_frame.pack(fill=BOTH, pady=20,)

    bottom_frame = Frame(window)
    bottom_frame.pack()

    

    todos = supabase.table("todos").select("id, is_done, created_at, name, created_by").execute()
    showData(window, todos.data, session.user.email)

    window.mainloop()

if __name__ == "__main__":
    supabase = config()
    main_window(supabase.auth.sign_in_with_password({ "email": "wiktor.w306@gmail.com", "password": "WikWie123"}), supabase)