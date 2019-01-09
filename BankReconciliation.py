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

class BankReconciliation():
    def __init__(self,bankDF,ledgerDF):
        self.bankDF = bankDF
        self.ledgerDF = ledgerDF
        self.solution = {}

        self.bankDF['Date'] = pd.to_datetime(bankDF['Date'])
        self.ledgerDF['Date'] = pd.to_datetime(ledgerDF['Date'])

        self.bankDF['associate'] = pd.Series()
        self.ledgerDF['associate'] = pd.Series()

        #Should have something automatic detect Description or Item
        bankColName = self.seperate_word(self.bankDF,"Description")
        ledgerColName = self.seperate_word(self.ledgerDF,"Item")

        (self.bankDF , self.onlyNSF) = self.remove_nsf(bankDF,"Description")

        self.bankDF = bankDF.reset_index()
        self.ledgerDF = ledgerDF.reset_index()


        self.matching(ledgerDF,bankDF,ledgerColName,bankColName)

    def printBankDF(self):
        print(self.bankDF)

    def printLedgerDF(self):
        print(self.ledgerDF)

    def printSolution(self):
        print(self.solution)

    def seperate_word(self, df, column_name):
        """Create new Dataframe Column with separate word"""
        word_sep = []
        for index, row in df.iterrows():
            word_sep.append([x.lower() for x in list(row[column_name])])
            df[str(column_name)+'_sep'] = pd.Series(word_sep)
        return str(column_name)+'_sep'
    
    def compare_list(self, list_word1, list_word2):
        """Compare set of word and return score"""
        score = 0
        set1 = set(list_word1)
        set2 = set(list_word2)
        for x in set1:
            for y in set2:
                if(x==y):
                    score = score + 1
        return score

    def remove_nsf(self, df, colname):
        _df = df[~df[colname].str.contains("NSF")]
        __df = df[df[colname].str.contains("NSF")]
        return _df,__df

    def associate(self, df, o, d):
        """associate, a = origin_index, b = destination_index"""
        if(len(df.loc[df['associate'] == d]) == 1):
            print('this destination index', str(d) , 'already has reconciled')
        else:
            df['associate'][o] = d

    def matching(self, ledgerDF, bankDF, ledgerCol, bankCol):
        series = ledgerDF[ledgerCol]
        series2 = bankDF[bankCol]
        for row2 in series2.iteritems():
            best_score = 0
            cur_score = 0
            for row in series.iteritems():
                cur_score = self.compare_list(row2[1],row[1])
                if cur_score > best_score :
                    best_score = cur_score
                    best_row = row
            self.associate(self.bankDF,row2[0],best_row[0])
            print("BEST ARE ",row2[0] ,row2[1]," BY ",best_row[0], best_row[1]," SCORE= ",best_score)









# reconciled = GUI(bank,ledger)

# reconciled.printBankDF()

# print(reconciled.bankDF['associate'])

# seperate_word(ledger,"Item")
# seperate_word(bank,"Description")

# (bank_no_nsf ,nsf_df) = remove_nsf(bank,"Description")

# ledger['associate'] = pd.Series()
# bank_no_nsf['associate'] = pd.Series()

# matching(ledger,bank_no_nsf,"Item_sep","Description_sep")

# print(bank_no_nsf)
# print(ledger)
