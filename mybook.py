from tkinter import Tk, Button, Label, Scrollbar, Listbox, StringVar, Entry, N, S, W, E, END
from tkinter import ttk
from tkinter import messagebox

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


# running the application
root.mainloop()