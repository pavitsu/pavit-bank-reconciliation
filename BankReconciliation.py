import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import tkinter as tk
from tkinter import ttk, scrolledtext, Menu, \
                    messagebox as msg, Spinbox, \
                    filedialog
global sol,f1Var,filePathBank,\
        filePathLedger,filePathBank, \
        intRad, intChk
filePathBank = ""
filePathLedger = ""

class BankReconciliation():
    def __init__(self, bankDF, ledgerDF):
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

        #Has to specific Name that contain NSF Problem
        (self.bankDF , self.onlyNSF) = self.remove_nsf(bankDF,"Description")

        # self.bankDF = self.bankDF.reset_index()
        self.ledgerDF = self.ledgerDF.reset_index()

        self.check_number(self.ledgerDF, self.bankDF)

        self.matching(self.ledgerDF,self.bankDF,ledgerColName,bankColName)
        
        # get NSF cheque row back & correct index
        __list = [self.bankDF, self.onlyNSF]
        self.bankDF = pd.concat(__list)
        self.bankDF = self.bankDF.reset_index()

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
        # Check if that original already has value?
        if (pd.isnull(df['associate'][o]) == False):
            print(' original index', str(o) , 'already has reconciled')
        # Check If destination index already used or not?
        elif(len(df.loc[df['associate'] == d]) == 1):
            print(' destination index', str(d) , 'already has reconciled')
        else:
            df['associate'][o] = int(d)

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
            print("BEST ARE ", row2[0],''.join(row2[1]) ," BY ", best_row[0],''.join(best_row[1])," SCORE= ",best_score)
    
    def check_number(self, ledgerDF, bankDF):
        for indexBank, rowBank in bankDF.iterrows():
            for indexLedger, rowLedger in ledgerDF.iterrows():
                boolDate = rowBank['Date'] == rowLedger['Date']
                boolMoneyIn = str(rowBank['Deposits']) == str(rowLedger['Debit'])
                boolMoneyOut = str(rowBank['Withdrawals']) == str(rowLedger['Credit'])
                if( boolDate and boolMoneyIn  and boolMoneyOut ):
                    print("compare by date, money.. "+ str(indexBank) \
                        +" equal to " + str(indexLedger))
                    self.associate(self.bankDF,indexBank,indexLedger)
                    break

if __name__ == "__main__":
    print("Please, Execute code from GUI_class.py")
