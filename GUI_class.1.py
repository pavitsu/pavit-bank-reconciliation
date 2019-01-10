'''
Jan 2019
@author: Pavit Suwansiri
'''
#======================
# imports
#======================
from BankReconciliation import BankReconciliation
import ast
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import tkinter as tk
from tkinter import ttk, scrolledtext, Menu, \
                    messagebox as msg, Spinbox, \
                    filedialog, MULTIPLE, EXTENDED
from time import  sleep         # careful - this can freeze the GUI
global sol,f1Var,filePathBank,\
        filePathLedger,filePathBank, \
        intRad, intChk
filePathBank = ""
filePathLedger = ""
# bankDF = pd.read_csv("~/Documents/GitHub/senior-bank-reconcile/example-data/bank-v2.csv")
# result_bank = pd.read_csv("~/Documents/GitHub/senior-bank-reconcile/example-data/bank-test")
# ledgerDF = pd.read_csv("~/Documents/GitHub/senior-bank-reconcile/example-data/ledger-v2.csv")
# result_ledger = pd.read_csv("~/Documents/GitHub/senior-bank-reconcile/example-data/ledger-test")
#=================================================================== 
class GUI(BankReconciliation):
    def __init__(self):
        self.setupWindow()
        self.initUploadScreen()
        self.initUI()
        bankDF = pd.read_csv(filePathBank)
        ledgerDF = pd.read_csv(filePathLedger)
        self.reconciled = BankReconciliation(bankDF,ledgerDF)
        # ***** Static Column Name Problem
        tempCol = self.reconciled.bankDF['associate']
        tempCol.fillna(-1,inplace=True)
        tempCol = tempCol.astype(np.int64)
        print(tempCol)
        sol = list(tempCol)

        self.set_solution(sol)
        self.setupWindow()
        self.planning_data(self.reconciled.bankDF,self.reconciled.ledgerDF,sol)
        self.initUI()

    def setupWindow(self):
        self.win = tk.Tk()   
        self.win.title("Python GUI")

    def set_solution(self, solution):
        global sol
        sol = solution

    def initUI(self):
        self.win.mainloop()
    
    def clickUpload(self):
        self.__filePath = filedialog.askopenfilename()
        if self.__filePath is None:
            return
        else:
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
        t = tk.Toplevel(self.win)
        t.wm_title("Window")
        tabControl = ttk.Notebook(t)
        # Tab Match
        def saveSelection():
            __str = lb1.curselection()
            resultSelect.configure(text=str(__str))
            indexBank = self.f1Var.get()
            sol[indexBank] = list(__str)

            # Senting updated value to  MainPage
            __str2 = "update{0}".format(indexBank)
            __str3 = """"""
            for value in sol[indexBank]:
                row = self.reconciled.ledgerDF.iloc[value]
                # Static Name Problem
                __temp = str(str(row["Date"])+\
                    ","+str (row["Item"])+\
                    ","+str(row["Debit"])+\
                    ","+str(row["Credit"])+\
                    ","+str(row["Balance"]))
                __str3 = __str3 + __temp + '\n'
                # print(__str3)
            
            d2[__str2].configure(text=str(__str3))
            print("Saved Selection", sol[indexBank], __str)
            print(sol)
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1,text="Match")
        lb1 = tk.Listbox(tab1,selectmode=MULTIPLE,width=70)
        for index, row in self.reconciled.ledgerDF.iterrows(): 
            # Static Name Column Problem ****
            lb1.insert(index,\
                (row["Date"]\
                ,row["Item"]\
                ,row["Debit"]\
                ,row["Credit"]\
                ,row["Balance"]))
        resultSelect = ttk.Label(t)
        bt = ttk.Button(tab1, text="Save Selection", command=saveSelection)

        # Tab Create
        def saveCreate():
            __list = [what.get(), why.get(), who.get()]
            indexBank = self.f1Var.get()
            sol[indexBank] = __list
            __str2 = "update{0}".format(indexBank)
            d2[__str2].configure(text=str(__list))
            print(__list)
            print(sol)
            pass
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2,text="Create")

        ## What
        what = tk.StringVar()
        tk.Label(tab2, text="What").pack()
        ttk.Entry(tab2, textvariable=what).pack()
        ## Why
        why = tk.StringVar()
        tk.Label(tab2, text="Why").pack()
        ttk.Entry(tab2, textvariable=why).pack()
        ## Who
        who = tk.StringVar()
        tk.Label(tab2, text="Who").pack()
        ttk.Entry(tab2, textvariable=who).pack()

        ttk.Button(tab2, text="Save Create", command=saveCreate).pack()

        # Tab Transfer
        def saveTransfer():
            __list = [bankAccount.get(), reference.get()]
            indexBank = self.f1Var.get()
            sol[indexBank] = __list
            __str2 = "update{0}".format(indexBank)
            d2[__str2].configure(text=str(__list))
            print(__list)
            print(sol)            
            pass
        tab3 = ttk.Frame(tabControl)
        tabControl.add(tab3,text="Transfer")
        ## Bank Account
        bankAccount = tk.StringVar()
        tk.Label(tab3,text="Bank Acccount").pack()
        ttk.Entry(tab3, textvariable=bankAccount).pack()
        ## Reference
        reference = tk.StringVar()
        tk.Label(tab3,text="Reference").pack()
        ttk.Entry(tab3,textvariable=reference).pack()
        ttk.Button(tab3,text="Save Transfer",command=saveTransfer).pack()

        # Tab Discuss
        def saveDiscuss():
            __list = [comment.get()]
            indexBank = self.f1Var.get()
            sol[indexBank] = __list
            __str2 = "update{0}".format(indexBank)
            d2[__str2].configure(text=str(__list))
            print(__list)
            print(sol)            
            pass
        comment = tk.StringVar()
        tab4 = ttk.Frame(tabControl)
        tabControl.add(tab4,text="Discuss") 
        tk.Label(tab4, text="Comment").pack()
        ttk.Entry(tab4,width=50,textvariable=comment).pack()
        ttk.Button(tab4, text="Save Discuss", command=saveDiscuss).pack()      

        lb1.pack()
        resultSelect.pack()
        bt.pack()
        tabControl.pack(expan=1, fill="both")
        self.win.mainloop()
        
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
        def saveToFile():
            path = filedialog.asksaveasfilename()
            if path is '':
                pass
            else:
                _file = open(path,'w+')
                _file.write(str(sol))
                print(str(sol))
                _file.close()

        def loadFromFile():
            path = filedialog.askopenfilename()
            if path is '':
                pass
            else:
                ("loading..." + str(path))
                _file = open(path,'r')
                txt = _file.read()
                _file.close()
                sol = ast.literal_eval(txt)
                print("set sol = " + str(sol))

            
        global d1;d1 = {}
        global d2;d2 = {}
        global sol; self.solution = solution
        self.frame1 = ttk.LabelFrame(self.win, text="Layout 1")
        self.frame1.grid(column=0, row=0)
        self.f1Var = tk.IntVar()
        for index, row in self.reconciled.bankDF.iterrows():
            __str = "variable{0}".format(index)
            d1[__str+"_button"] = tk.Radiobutton(self.frame1, variable=self.f1Var, value = index )
            d1[__str+"_button"].grid(column=0, row=index, sticky=tk.W)
            # Fixed Selection Name Problem
            ttk.Label(self.frame1, text=str(row["Date"])).grid(column=1, row=index)
            ttk.Label(self.frame1, text=str(row["Description"])).grid(column=2, row=index)
            ttk.Label(self.frame1, text=str(row["Withdrawals"])).grid(column=3, row=index)
            ttk.Label(self.frame1, text=str(row["Deposits"])).grid(column=4, row=index)
            ttk.Label(self.frame1, text=str(row["Balance"])).grid(column=5, row=index)
            ttk.Label(self.frame1, text=str(row["associate"])).grid(column=6, row=index)
            __str2 = "update{0}".format(index)
            d2[__str2] = ttk.Label(self.frame1)
            d2[__str2].grid(column=7, row=index)
        editButton = ttk.Button(self.win, text="Edit", command=self.editTransaction)
        editButton.grid(column=0, row=1)
        saveButton = ttk.Button(self.win, text="Save To File...", command=saveToFile)
        saveButton.grid(column=0, row=2)
        loadButton = ttk.Button(self.win, text="Load File...",command=loadFromFile)
        loadButton.grid(column=0, row=3)
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

# ui = GUI()
if __name__ == "__main__":
    ui = GUI()