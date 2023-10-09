# importing whole module
from tkinter import *
from tkinter.ttk import *
 
# importing strftime function to
# retrieve system's time
from time import strftime
 
def cloaks():
    root = Tk()
    root.title('Clock')
    def cloak():
        string = strftime('%H:%M:%S %p')
        lbl.config(text=string)
        lbl.after(1000, cloak)
 
    lbl = Label(root, font=('calibri', 40, 'bold'),
            background='purple',
            foreground='white')
    lbl.pack(anchor='center')
    cloak()
    mainloop()
