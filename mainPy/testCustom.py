import tkinter as tk
from tkinter import ttk

root = tk.Tk()

combostyle = ttk.Style()

combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': 'blue',
                                       'fieldbackground': 'red',
                                       'background': 'green'
                                       }}}
                         )
# ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox
combostyle.theme_use('combostyle') 

# show the current styles
# print(combostyle.theme_names())

combo = ttk.Combobox(root, values=['1', '2', '3'])
combo['state'] = 'readonly'
combo.pack()

entry = tk.Entry(root)
entry.pack()

root.mainloop()