import pandas as pd
import numpy as np
import warnings
from pandas import isnull
warnings.filterwarnings('ignore')

class BankReconciliation():
    def __init__(self, listBankDF, listLedgerDF, normalCheck = False, nameCheck = False):

        for (index,df) in enumerate(listBankDF):
            df['Bank_Entity'] = str(index)

        for (index,df) in enumerate(listLedgerDF):
            df['Ledger_Entity'] = str(index)
        
        self.bankDF = pd.concat(listBankDF)
        self.ledgerDF = pd.concat(listLedgerDF)
        self.bankDF = self.bankDF.reset_index(drop=True)
        self.ledgerDF = self.ledgerDF.reset_index(drop=True)
        self.solution = {}

        self.bankDF['Date'] = pd.to_datetime(self.bankDF['Date'])
        self.ledgerDF['Date'] = pd.to_datetime(self.ledgerDF['Date'])

        self.bankDF['associate'] = np.nan
        self.ledgerDF['associate'] = np.nan

        self.bankDF['Description'] = self.bankDF['Description'].astype(str)
        self.ledgerDF['Item'] = self.ledgerDF['Item'].astype(str)

        #Should have something automatic detect Description or Item
        bankColName = self.seperate_word(self.bankDF,"Description")
        ledgerColName = self.seperate_word(self.ledgerDF,"Item")

        #Has to specific Name that contain NSF Problem
        (self.bankDF , self.onlyNSF) = self.remove_nsf(self.bankDF,"Description")

        # self.bankDF = self.bankDF.reset_index()
        self.ledgerDF = self.ledgerDF.reset_index()

        if (normalCheck): self.check_number(self.ledgerDF, self.bankDF)
        if (nameCheck): self.matching(self.ledgerDF,self.bankDF,ledgerColName,bankColName)
        
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
        # print(df['associate'][o])
        if (not (isnull(df['associate'][o]))):
            print(' original index', str(o) , 'already has reconciled')
        # Check If destination index already used or not?
        elif(len(df.loc[df['associate'] == d]) == 1):
            print(' destination index', str(d) , 'already has reconciled')
        else:
            df['associate'][o] = int(d)

    def matching(self, ledgerDF, bankDF, ledgerCol, bankCol):
        print("Doing name item check....")
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
        #######
        # print(bankDF)
        # print("Doing normal check....")
        # print(ledgerDF)
        #######
        for indexBank, rowBank in bankDF.iterrows():
            for indexLedger, rowLedger in ledgerDF.iterrows():
                boolDate = rowBank['Date'] == rowLedger['Date']
                rowDeposit = float(str(rowBank['Deposits']).replace(',',''))
                rowDebit = float(str(rowLedger['Debit']).replace(',',''))
                rowWithdrawals = float(str(rowBank['Withdrawals']).replace(',',''))
                rowCredit = float(str(rowLedger['Credit']).replace(',',''))
                if(isnull(rowDeposit) & isnull(rowDebit)):
                    boolMoneyIn =True
                else:boolMoneyIn = rowDeposit == rowDebit 
                if(isnull(rowWithdrawals) & isnull(rowCredit)):
                    boolMoneyOut = True
                else: boolMoneyOut = rowWithdrawals == rowCredit 
                ######
                # print(boolDate,rowBank['Date'] , rowLedger['Date'])
                # print(boolMoneyIn,float(str(rowBank['Deposits']).replace(',','')), float(str(rowLedger['Debit']).replace(',','')))
                # print(boolMoneyOut,float(str(rowBank['Withdrawals']).replace(',','')),float(str(rowLedger['Credit']).replace(',','')))
                ######
                if( boolDate and boolMoneyIn  and boolMoneyOut ):
                    print("compare by date, money.. "+ str(indexBank) \
                        +" equal to " + str(indexLedger))
                    self.associate(self.bankDF,indexBank,indexLedger)
                    break
                # else:print("not match")

if __name__ == "__main__":
    pass
    # print("Please, Execute code from GUI_class.py")
    # bankDF = pd.read_csv("/Users/pavitsu/Documents/GitHub/senior-bank-reconcile/example-data/bank-flower-rose.csv")
    # bankDF2 = pd.read_csv("/Users/pavitsu/Documents/GitHub/senior-bank-reconcile/example-data/bank2-flower-rose.csv")
    # ledgerDF = pd.read_csv("/Users/pavitsu/Documents/GitHub/senior-bank-reconcile/example-data/ledger-flower-rose.csv")
    # ledgerDF2 = pd.read_csv("/Users/pavitsu/Documents/GitHub/senior-bank-reconcile/example-data/ledger-flower-rose.csv")
    # auto = BankReconciliation([bankDF,bankDF2],[ledgerDF,ledgerDF2], normalCheck = True, nameCheck = True)