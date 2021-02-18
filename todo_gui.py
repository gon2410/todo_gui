#!/usr/bin/env python3

__author__ = "Gonzalo Olivera"
__email__ = "goonolivera@hotmail.com"

from datetime import date, datetime
import sqlite3
from sqlite3 import Error
import os
from tkinter import Tk, StringVar, Frame, Button, Label, Entry, Scrollbar, Listbox, Checkbutton, END, MULTIPLE, PhotoImage, messagebox

path = os.path.dirname(os.path.abspath(__file__))

class Task(object):
    def __init__(self, desc, date_add):
        self.desc = desc
        self.date_add = date_add

    def get_desc(self):
        return self.desc

    def get_date(self):
        return self.date_add


if os.path.isfile(path + "/task.db"):
    pass
else:
    try:
        conn = sqlite3.connect(path + "/task.db")
    except Error:
        messagebox.showerror(message=Error, title="Error")

    cursor = conn.cursor()

    cursor.execute("CREATE TABLE TASK(id integer PRIMARY KEY, desc text, date text)")

    conn.commit()
    conn.close()

def main():
    window = Tk()
    window.geometry('550x400')
    window.resizable(width=0, height=0)
    window.title("Todo")
    
    window.iconphoto(False, PhotoImage(file=path + "/Icons/icon.png"))

    def list_tasks():
        try:
            conn = sqlite3.connect(path + "/task.db")
        except Error:
            messagebox.showerror(message=Error, title="Error")

        cursor = conn.cursor()
        cursor.execute("SELECT desc FROM TASK")
        descs = cursor.fetchall()

        for desc in descs:
            lis.insert(END, desc[-1])

    def update_task_list():
        lis.delete(0, END)
        list_tasks()

    def delete():
        selected_task = lis.curselection()
        all_task = lis.get(0, END)
        sel_task = [all_task[task] for task in selected_task]
        
        try:
            conn = sqlite3.connect(path + "/task.db")
        except Error:
            messagebox.showerror(message=Error, title="Error")

        cursor = conn.cursor()
        for i in sel_task:
            cursor.execute("DELETE FROM TASK WHERE desc=?", (i,))
            conn.commit()
        conn.close()

        update_task_list()

    task_entry = StringVar()
    def get_entry():

        # get date and time
        date_now = date.today()
        time = datetime.now()
        
        # get user input
        desc = task_entry.get()

        # conditional to make sure that the string is not empty (it'd be stupid to add an empty string to database)
        if len(desc) != 0:
            task = Task(desc, date_now.strftime("%B %d, %Y") + " - " + time.strftime("%H:%M"))

            # should create a dialog that shows the error (if there's any)
            try:
                conn = sqlite3.connect(path + "/task.db")
            except Error:
                messagebox.showerror(message=Error, title="Error")

            cursor = conn.cursor()

            cursor.execute("SELECT id FROM TASK")
            ids = cursor.fetchall()

            # always diferent id numbers (not sure if an id number it's necessary but I will leave it for now)
            if len(ids) == 0:
                values = (1, task.get_desc(), task.get_date())
            else:
                values = (list(ids[-1])[-1] + 1, task.get_desc(), task.get_date())

            cursor.execute("INSERT INTO TASK(id, desc, date) VALUES(?, ?, ?)", values)
            conn.commit()
            conn.close()
            
            # updating task list after adding new task
            update_task_list()

    # creating entry and buttons with their respective function
    Entry(window, textvariable=task_entry).place(x=1, y=1, width=200, height=25)

    Button(window, text="Add", command=get_entry).place(x=210, y=1, height=25)

    trash_icon = PhotoImage(file=path + "/Icons/trash.png")
    Button(window, text="Delete", command=delete, image=trash_icon).place(x=520, y=15)
    
    quit_icon = PhotoImage(file=path + "/Icons/quit.png")
    Button(window, text="Exit", command=quit, image=quit_icon).place(x=518, y=367)
    
    # creating scrollbar
    scrollbar = Scrollbar(window)
    scrollbar.pack(side="right", fill="none")
    
    # creating listbox
    lis = Listbox(window, width=530, height=320, bg="white", selectmode=MULTIPLE, font=("normal", 12))
    lis.pack(padx=0, pady=50)
    lis.config(yscrollcommand = scrollbar.set)

    scrollbar.config(command=lis.yview)



    # listing task list when the user opens the program
    list_tasks()

    window.mainloop()


if __name__ == "__main__":
    main()
