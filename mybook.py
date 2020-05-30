from tkinter import Tk, Button, Label, Scrollbar, Listbox, StringVar, Entry, N, S, W, E, END
from tkinter import ttk
from tkinter import messagebox

#################################
###### Connection to sqlserver database #####
######################################

from sqlserver_config import dbConfig
import pypyodbc as pyo

# connection to db
con = pyo.connect(**dbConfig)
# print(con)
# create cursor object (execute sql commads in python code with db.session)
cursor = con.cursor()

# 6.1  __init__
# при создании экземпляра класса происходит подключение к базе данных
# и создается объект курсора на печать выводиться( "You have connected to the  database" и объект соединения к бд)
# 6.2 метод __del__:
# закрытие соедиения с бд
# 6.3. метод view:
# возвращает все записи из таблицы books
# 6.4 метод insert:
# добавляет запись в бд
# 6.5. метод update
# обновляет запись в бд
# 6.6 метод delete:
# удаляет запись из  бд

class Bookdb():
    def __init__(self):
        self.con = pyo.connect(**dbConfig)
        self.cursor = self.con.cursor() # in original = con.cursor()
        print(self.con)
        print("You have connected to the database")

    def __del__(self):
        self.con.close()

    def view(self):
        self.cursor.execute("SELECT * FROM books;")
        rows = self.cursor.fetchall()
        return rows

    def insert(self, title, author, isbn):
        sql = 'INSERT INTO books(title, author, isbn) VALUES (?, ?, ?);'
        values = [title, author, isbn]
        self.cursor.execute(sql, values)
        self.con.commit()
        # Всплывающее окно-сообщение, что добавлена новая книга
        messagebox.showinfo(title="Book Database", message="New book added to database")

    def update(self, id, title, author, isbn):
        tsql = "UPDATE books SET title = ?, author = ?, isbn = ? WHERE id = ?"
        self.cursor.execute(tsql, [title, author, isbn, id])
        self.con.commit()
        messagebox.showinfo(title="Book Database", message="Book Updated")

    def delete(self, id):
        dsql = "DELETE FROM books WHERE id = ?"
        self.cursor.execute(dsql, [id])
        self.con.commit()
        messagebox.showinfo(title='Book Database', message="Book Deleted")


# main window of the application
root = Tk()

root.title('My books database application')
root.configure(background='light green')
root.geometry('850x500')
root.resizable(width=False, height=False)

# 1. Top row of elements of the screen
# 1.1.Title:
title_label = ttk.Label(root, text='Title: ', background='light green', font=('TkDefaultFont', 16))
title_label.grid(row=0, column=0, sticky=W)

title_text = StringVar()

title_entry = ttk.Entry(root, width=24, textvariable=title_text)
title_entry.grid(row=0, column=1, sticky=W)

# 1.2.Title:
author_label = ttk.Label(root, text='Author: ', background='light green', font=('TkDefaultFont', 16))
author_label.grid(row=0, column=2, sticky=W)

author_text = StringVar()

author_entry = ttk.Entry(root, width=24, textvariable=author_text)
author_entry.grid(row=0, column=3, sticky=W)

# 1.3.ISBN:

isbn_label = ttk.Label(root, text='ISBN: ', background='light green', font=('TkDefaultFont', 16))
isbn_label.grid(row=0, column=4, sticky=W)

isbn_text = StringVar()

isbn_entry = ttk.Entry(root, text=isbn_text)
isbn_entry.grid(row=0, column=5, sticky=W)

# 1.4.Button "Add Book"
add_btn = Button(root, text='Add book', bg='dark blue', fg='white', font='helvetica 10 bold', command='')
add_btn.grid(row=0, column=6, sticky=W)

# 2. ListBox:

# 2.1 listbox
list_box = Listbox(root, height=16, width=40, font='helvetica 13', bg='light blue')
list_box.grid(row=3, column=1, columnspan=14, sticky=W+E, padx=15, pady=40)

# 2.2 Scroll bar:
scroll = Scrollbar(root)
scroll.grid(row=1, column=8, rowspan=14, sticky=W)

# 2.3 Attach scroll_bar to the list_box:
list_box.configure(yscrollcommand=scroll.set)
scroll.configure(command=list_box.yview)

# 3. Bottom buttons ( 15 row  -  list box 1-14 rows)

view_all_btn = Button(root, text='View all records', bg='black', fg='white', font='helvetica 10 bold', command="")
view_all_btn.grid(row=15, column=1)

clear_screen_btn = Button(root, text='Clear Screen', bg='dark red', fg='white', font='helvetica 10 bold', command="")
clear_screen_btn.grid(row=15, column=2)

exit_app_btn = Button(root, text='Exit application', bg='blue', fg='white', font='helvetica 10 bold', command="")
exit_app_btn.grid(row=15, column=3)

modify_rec_btn = Button(root, text='Modify record', bg='purple', fg='white', font='helvetica 10 bold', command="")
modify_rec_btn.grid(row=15, column=4)

delete_rec_btn = Button(root, text='Delete record', bg='red', fg='white', font='helvetica 10 bold', command="")
delete_rec_btn.grid(row=15, column=5)


# running the application
root.mainloop()