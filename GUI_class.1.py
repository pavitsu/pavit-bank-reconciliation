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
global sol,f1Var,filePathBank,\
        filePathLedger,filePathBank, \
        intRad, intChk
filePathBank = ""
filePathLedger = ""
# bank = pd.read_csv("~/Documents/GitHub/senior-bank-reconcile/example-data/bank-v2.csv")
result_bank = pd.read_csv("~/Documents/GitHub/senior-bank-reconcile/example-data/bank-test")
# ledger = pd.read_csv("~/Documents/GitHub/senior-bank-reconcile/example-data/ledger-v2.csv")
result_ledger = pd.read_csv("~/Documents/GitHub/senior-bank-reconcile/example-data/ledger-test")
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

    def nextClicked(self):
        self.win.destroy()

    def editTransaction(self):
        def insertElement(listbox, index, value):
            listbox.insert(index, value)
            pass
        t = tk.Toplevel(self.win)
        t.wm_title("Window")
        Lb1 = tk.Listbox(t)
        for index, row in self.ledger.iterrows(): 

        
        # 
        # Lb1.insert(2, "Perl")
        # Lb1.insert(3, "C")
        # Lb1.insert(4, "PHP")
        # Lb1.insert(5, "JSP")
        # Lb1.insert(6, "Ruby")

        # Lb1.pack()
        pass
    ####################### DELETE THIS
    def create_window(self):
        counter = 1
        t = tk.Toplevel(self.win)
        
        l = tk.Label(t, text="This is window #%s" % counter)
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)
    ########################
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
        self.frame1 = ttk.LabelFrame(self.win, text="Layout 1")
        self.frame1.grid(column=0, row=0)
        self.f1Var = tk.IntVar()
        
            __str = "variable{0}".format(index)
            self.d1[__str+"_button"] = tk.Radiobutton(self.frame1, variable=self.f1Var, value = index )
            self.d1[__str+"_button"].grid(column=0, row=index, sticky=tk.W)
            for i in range(len(df.columns)):
                ttk.Label(self.frame1, text=str(row[i])).grid(column=i+1, row=index) 

        editButton = ttk.Button(self.win, text="Edit", command=self.editTransaction)
        editButton.grid(column=0, row=1)
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

        self.nextButton = ttk.Button(self.frame2, text="Next...", command=self.nextClicked)
        self.nextButton.grid(column=0,row = 1)

        pass


sol = [0,6,1,2,None,4,None,None,None,7]
ui = GUI()

# ui.initUploadScreen()
# ui.initUI()

ui.set_solution(sol)
ui.planning_data(result_bank,result_ledger,sol)
ui.initUI()