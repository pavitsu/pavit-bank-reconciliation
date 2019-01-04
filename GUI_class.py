'''
Jan 2019
@author: Pavit Suwansiri
'''
#======================
# imports
#======================
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import tkinter as tk
from tkinter import ttk, scrolledtext, Menu, \
                    messagebox as msg, Spinbox
from time import  sleep         # careful - this can freeze the GUI
global sol
global f1Var
#=================================================================== 
class GUI():
    def __init__(self):         # Initializer method
        # Create instance
        self.win = tk.Tk()   
        
        # Add a title       
        self.win.title("Python GUI")      

    def set_solution(self, solution):
        global sol
        sol = solution

    def initUI(self):
        self.win.mainloop()

    def selecting_button(self, solution):
        for i in range(len(solution)):
            if solution[i] is not None:
                __temp = "variable{0}".format(solution[i])
                self.d2[__temp+"_button"].select()
                print(__temp+"_button selected")

    def interact_with_checkbox(self):
        for index,target in enumerate(sol):
            print("interacting...")
            __str2 = "variable{0}".format(target)
            __value=self.f1Var.get()
            print(index, ":", target)
            if __value == index:
                try:
                    self.d2[__str2+"_button"].configure(state="active")
                except KeyError as identifier:
                    continue
            elif target is not None:
                self.d2[__str2+"_button"].configure(state="disabled") 
            else:
                continue


    def planning_data(self,df,df2,solution):
        global d1;self.d1 = {}
        global d2;self.d2 = {}
        global sol; self.solution = solution
        self.frame2 = ttk.LabelFrame(self.win, text="Layout 2")
        self.frame2.grid(column=0, row=1) 
        for index, row in df2.iterrows():
            __str2 = "variable{0}".format(index)
            self.d2[__str2]= tk.IntVar()
            self.d2[__str2+"_button"] = tk.Checkbutton(self.frame2, variable=__str2)
            self.d2[__str2+"_button"].grid(column=0, row=index, sticky=tk.W)
            for i in range(len(df.columns)):
                ttk.Label(self.frame2, text=str(row[i])).grid(column=i+1, row=index)
        self.frame1 = ttk.LabelFrame(self.win, text="Layout 1")
        self.frame1.grid(column=0, row=0)
        self.f1Var = tk.IntVar()
        for index, row in df.iterrows(): 
            __str = "variable{0}".format(index)
            self.d1[__str+"_button"] = tk.Radiobutton(self.frame1, variable=self.f1Var, value = index ,command = self.interact_with_checkbox)
            self.d1[__str+"_button"].grid(column=0, row=index, sticky=tk.W)
            for i in range(len(df.columns)):
                ttk.Label(self.frame1, text=str(row[i])).grid(column=i+1, row=index) 
        self.selecting_button(solution)
        print("Done! Planning Data!")
        pass