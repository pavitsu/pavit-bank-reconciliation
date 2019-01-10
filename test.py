from tkinter import *
from tkinter import ttk


root = Tk()

Label(root, text="hello").pack()

top1 = Toplevel(root)

Label(top1, text="top1 level").pack()

tabControl = ttk.Notebook(top1)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1,text="tab1")
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2,text="tab2")
tab3 = ttk.Frame(tabControl)
tabControl.add(tab3,text="tab3")

tabControl.pack(expan=1, fill="both")
root.mainloop
