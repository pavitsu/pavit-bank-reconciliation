import Tkinter as tk


class App:
    def __init__(self):
        self.root=tk.Tk()
        self.vsb = tk.Scrollbar(orient="vertical", command=self.OnVsb)
        self.lb1 = tk.Listbox(self.root, yscrollcommand=self.vsb.set)
        self.lb2 = tk.Listbox(self.root, yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right",fill="y")
        self.lb1.pack(side="left",fill="x", expand=True)
        self.lb2.pack(side="left",fill="x", expand=True)
        self.lb1.bind("<MouseWheel>", self.OnMouseWheel)
        self.lb2.bind("<MouseWheel>", self.OnMouseWheel)
        for i in range(100):
            self.lb1.insert("end","item %s" % i)
            self.lb2.insert("end","item %s" % i)
        self.root.mainloop()

    def OnVsb(self, *args):
        self.lb1.yview(*args)
        self.lb2.yview(*args)

    def OnMouseWheel(self, event):
        self.lb1.yview("scroll", event.delta,"units")
        self.lb2.yview("scroll",event.delta,"units")
        # this prevents default bindings from firing, which
        # would end up scrolling the widget twice
        return "break"


from Tkinter import *

master = Tk()

scrollbar = Scrollbar(master)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(master, yscrollcommand=scrollbar.set)
for i in range(1000):
    listbox.insert(END, str(i))
listbox.pack(side=LEFT, fill=BOTH)

scrollbar.config(command=listbox.yview)

mainloop()

# app=App()