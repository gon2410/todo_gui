#!/usr/bin/env python3

__author__ = "Gonzalo Olivera"
__email__ = "goonolivera@hotmail.com"

from datetime import date, datetime
import sqlite3
from sqlite3 import Error
import os
from tkinter import Tk, StringVar, Frame, Button, Label, Entry, Scrollbar, Listbox, Checkbutton, END, MULTIPLE, PhotoImage, messagebox, Menu, Toplevel
import json

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
    window.geometry('650x400')
    window.resizable(width=0, height=0)
    window.title("Todo")
    #window.config(background = "#000000")
    window.iconphoto(False, PhotoImage(file=path + "/Icons/icon.png"))

    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=0)
    #filemenu.add_command(label="Settings", command=config_window)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="File", menu=filemenu)


    def apply_configs():
        a_file = open(path + "/config_file.json", 'r')
        json_object = json.load(a_file)
        a_file.close()

        my_entry.config(fg=json_object['my_entry']['fg'])
        my_entry.config(bg=json_object['my_entry']['bg'])

        add_button.config(text=json_object['add_button']["text"])
        add_button.config(borderwidth=json_object['add_button']["borderwidth"])
        add_button.config(highlightthickness=json_object['add_button']["highlightthickness"])
        add_button.config(fg=json_object['add_button']["fg"])
        add_button.config(bg=json_object['add_button']["bg"])
        add_button.config(activeforeground=json_object['add_button']["activeforeground"])
        add_button.config(activebackground=json_object['add_button']["activebackground"])

        delete_button.config(text=json_object['delete_button']["text"])
        delete_button.config(borderwidth=json_object['delete_button']["borderwidth"])
        delete_button.config(highlightthickness=json_object['delete_button']["highlightthickness"])
        delete_button.config(fg=json_object['delete_button']["fg"])
        delete_button.config(bg=json_object['delete_button']["bg"])
        delete_button.config(activeforeground=json_object['delete_button']["activeforeground"])
        delete_button.config(activebackground=json_object['delete_button']["activebackground"])

        update_button.config(text=json_object['update_button']["text"])
        update_button.config(borderwidth=json_object['update_button']["borderwidth"])
        update_button.config(highlightthickness=json_object['update_button']["highlightthickness"])
        update_button.config(fg=json_object['update_button']["fg"])
        update_button.config(bg=json_object['update_button']["bg"])
        update_button.config(activeforeground=json_object['update_button']["activeforeground"])
        update_button.config(activebackground=json_object['update_button']["activebackground"])

        lis.config(fg=json_object['lis']['fg'])
        lis.config(bg=json_object['lis']['bg'])

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
            my_entry.delete(0, END)
            # updating task list after adding new task
            update_task_list()

    

    # creating entry and buttons with their respective function
    my_entry = Entry(window, textvariable = task_entry)
    my_entry.place(x=5, y=20, width=200, height=25)

    add_button = Button(window, command = get_entry)
    add_button.place(x=210, y=20, height=25)

    delete_button = Button(window, command=delete)
    delete_button.place(x=582, y=20)

    update_button = Button(window, command=apply_configs)
    update_button.place(x=580, y=371)

    # creating scrollbar
    scrollbar = Scrollbar(window)
    scrollbar.pack(side="right", fill="none")

    # creating listbox (mini window where tasks are listed)
    lis = Listbox(window,
                  width=530,
                  height=320,
                  selectmode=MULTIPLE,
                  font=("normal", 12))
    lis.pack(padx=5, pady=50)
    lis.config(yscrollcommand = scrollbar.set)

    scrollbar.config(command=lis.yview)

    # listing task list when the user opens the program
    apply_configs()
    list_tasks()

    window.config(menu=menubar)
    window.mainloop()


if __name__ == "__main__":
    main()