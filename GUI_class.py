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
import tkinter as tk
from tkinter import ttk, scrolledtext, Menu, \
                    messagebox as msg, Spinbox, \
                    filedialog
from time import  sleep         # careful - this can freeze the GUI
global sol
global f1Var
global filePathBank
global filePathLedger
filePathBank = ""
filePathLedger = ""
# bank = pd.read_csv("~/Documents/GitHub/senior-bank-reconcile/example-data/bank-v2.csv")
# result_bank = pd.read_csv("~/Documents/GitHub/senior-bank-reconcile/example-data/bank-test")
# ledger = pd.read_csv("~/Documents/GitHub/senior-bank-reconcile/example-data/ledger-v2.csv")
# result_ledger = pd.read_csv("~/Documents/GitHub/senior-bank-reconcile/example-data/ledger-test")
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
    
    def clickUpload(self):
        self.__filePath = filedialog.askopenfilename()
        self.enteredfilePath.configure(text= self.__filePath)
        global filePathBank
        filePathBank = self.__filePath
        print("filePath = " + filePathBank)

    def clickUpload2(self):
        self.__filePath = filedialog.askopenfilename()
        if self.__filePath is None:
            return
        else:
            self.enteredFilePath2.configure(text= self.__filePath)
            global filePathLedger
            filePathLedger = self.__filePath
            print("filePath2 = " + filePathLedger)

    def NextClicked(self):
        self.win.destroy()

    def selecting_button(self, solution):
        for i in range(len(solution)):
            if solution[i] is not None:
                __temp = "variable{0}".format(solution[i])
                self.d2[__temp+"_button"].select()
                print(__temp+"_button selected")

    def interact_with_checkbox(self):
        '''GUI function used in planning_data function,
        radiobutton so it can auto disabled/active checkbox on Ledger side
        '''
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
        '''
        run this for GUI for after processing CSV file automated, 
        Goal are shown as table for user can edit to correct result
        df, Bank Statement DataFrame 
        df2, Ledger DataFrame
        solution, list eg. [0,6,1,2,None,4,None,None,None,7]
        which represent (solution, index 0 contain 0) meaning ...
        ...(df row 0) are reconcile with (df2 row 0)
        '''
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

    def initUploadScreen(self):
        '''run this for GUI for request user to input CSV file uploading'''
        self.frame1 = ttk.LabelFrame(self.win, text="Bank Statement")
        self.frame1.grid(column=0 , row=0)
        self.actionBrowse = ttk.Button(self.frame1, text="Browse...", command=self.clickUpload)
        self.actionBrowse.grid(column=1, row=0)
        self.enteredfilePath = tk.Label(self.frame1, width=50)
        self.enteredfilePath.grid(column=0, row=0)

        self.frame2 = ttk.LabelFrame(self.win, text="Ledger")
        self.frame2.grid(column=0 , row=1)
        self.actionBrowse2 = ttk.Button(self.frame2, text="Browse...", command=self.clickUpload2)
        self.actionBrowse2.grid(column=1, row=0)
        self.enteredFilePath2 = tk.Label(self.frame2, width=50)
        self.enteredFilePath2.grid(column=0, row=0)

        self.nextButton = ttk.Button(self.frame2, text="Next...", command=self.NextClicked)
        self.nextButton.grid(column=0,row = 1)

        pass


# sol = [0,6,1,2,None,4,None,None,None,7]
# ui = GUI()

# ui.initUploadScreen()
# ui.initUI()

# ui.set_solution(sol)
# ui.planning_data(result_bank,result_ledger,sol)
# ui.initUI()