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

# Создаем экземпляр класса Bookdb.
db = Bookdb()

# Создание функций ( create a function for selected row inside Listbox)

def get_selected_row(event):
    '''This function shows title, author, isbn of the book
    chosen in the row of list box
    on the top panel of Gui'''
    global selected_tuple
    index = list_box.curselection()[0] # Метод curselection() позволяет получить в виде кортежа индексы выбранных элементов экземпляра Listbox.
    selected_tuple = list_box.get(index) # Кортеж из индекс, названия, автор и isbn
    title_entry.delete(0, 'end') # Очистка окна title
    title_entry.insert('end', selected_tuple[1]) # вставка названия выбранной книги.
    author_entry.delete(0, 'end')
    author_entry.insert('end', selected_tuple[2])
    isbn_entry.delete(0, 'end')
    isbn_entry.insert('end', selected_tuple[3])


def view_records():
    list_box.delete(0, 'end')
    for row in db.view():
        list_box.insert('end', row)


def add_book():
    db.insert(title_text.get(), author_text.get(), isbn_text.get())
    list_box.delete(0, 'end')
    list_box.insert('end', (title_text.get(), author_text.get(), isbn_text.get()))
    title_entry.delete(0, 'end')
    author_entry.delete(0, 'end')
    isbn_entry.delete(0, 'end')
    con.commit()


def delete_records():
    db.delete(selected_tuple[0])
    con.commit() # считаю, что не нужно, так как комит встроен в метод db.delete


def clear_sreen():
    list_box.delete(0, 'end')
    title_entry.delete(0, 'end')
    author_entry.delete(0, 'end')
    isbn_entry.delete(0, 'end')


def update_records():
    db.update(selected_tuple[0], title_text.get(), author_text.get(), isbn_text.get())
    title_entry.delete(0, 'end')
    author_entry.delete(0, 'end')
    isbn_entry.delete(0, 'end')
    con.commit()

def on_closing():
    dd = db
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        del dd

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
add_btn = Button(root, text='Add book', bg='dark blue', fg='white', font='helvetica 10 bold', command=add_book)
add_btn.grid(row=0, column=6, sticky=W)

# 2. ListBox:

# 2.1 listbox
list_box = Listbox(root, height=16, width=40, font='helvetica 13', bg='light blue')
list_box.grid(row=3, column=1, columnspan=14, sticky=W+E, padx=15, pady=40)
list_box.bind('<<ListboxSelect>>', get_selected_row)

# 2.2 Scroll bar:
scroll = Scrollbar(root)
scroll.grid(row=1, column=8, rowspan=14, sticky=W)

# 2.3 Attach scroll_bar to the list_box:
list_box.configure(yscrollcommand=scroll.set)
scroll.configure(command=list_box.yview)

# 3. Bottom buttons ( 15 row  -  list box 1-14 rows)

view_all_btn = Button(root, text='View all records', bg='black', fg='white', font='helvetica 10 bold', command=view_records)
view_all_btn.grid(row=15, column=1)

clear_screen_btn = Button(root, text='Clear Screen', bg='dark red', fg='white', font='helvetica 10 bold', command=clear_sreen)
clear_screen_btn.grid(row=15, column=2)

exit_app_btn = Button(root, text='Exit application', bg='blue', fg='white', font='helvetica 10 bold', command=root.destroy)
exit_app_btn.grid(row=15, column=3)

modify_rec_btn = Button(root, text='Modify record', bg='purple', fg='white', font='helvetica 10 bold', command=update_records)
modify_rec_btn.grid(row=15, column=4)

delete_rec_btn = Button(root, text='Delete record', bg='red', fg='white', font='helvetica 10 bold', command=delete_records)
delete_rec_btn.grid(row=15, column=5)



# running the application
if __name__ == '__main__':
    root.mainloop()