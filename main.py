import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Get csv data
bank = pd.read_csv("~/Documents/GitHub/senior-bank-reconcile/example-data/bank-v2.csv")
ledger = pd.read_csv("~/Documents/GitHub/senior-bank-reconcile/example-data/ledger-v2.csv")

# Specific Which column are.... (Allow user to select)
# ...

# Correcting Format Data
bank['Date'] = pd.to_datetime(bank['Date'])
ledger['Date'] = pd.to_datetime(ledger['Date'])

bank = bank.reset_index()
ledger = ledger.reset_index()

def seperate_word(df, column_name):
        """Create new Dataframe Column with separate word"""
        word_sep = []
        for index, row in df.iterrows():
            word_sep.append([x.lower() for x in list(row[column_name])])
            df[str(column_name)+'_sep'] = pd.Series(word_sep)

def compare_list(list_word1, list_word2):
    """Compare set of word and return score"""
    score = 0
    set1 = set(list_word1)
    set2 = set(list_word2)
    for x in set1:
        for y in set2:
            if(x==y):
                score = score + 1
    return score

def remove_nsf(df,colname):
    _df = df[~df[colname].str.contains("NSF")]
    __df = df[df[colname].str.contains("NSF")]
    return _df,__df


def associate(df,o,d):
    """associate, a = origin_index, b = destination_index"""
    if(len(df.loc[df['associate'] == d]) == 1):
        print('this destination index', str(d) , 'already has reconciled')
    else:
        df['associate'][o] = d

def matching(book,bank,colname,colname2):
    series = book[colname]
    series2 = bank[colname2]
    for row2 in series2.iteritems():
        best_score = 0
        cur_score = 0
        for row in series.iteritems():
            cur_score = compare_list(row2[1],row[1])
            if cur_score > best_score :
                best_score = cur_score
                best_row = row
        associate(bank,row2[0],best_row[0])
        print("BEST ARE ",row2[0] ,row2[1]," BY ",best_row[0], best_row[1]," SCORE= ",best_score)


seperate_word(ledger,"Item")
seperate_word(bank,"Description")

(bank_no_nsf ,nsf_df) = remove_nsf(bank,"Description")

ledger['associate'] = pd.Series()
bank_no_nsf['associate'] = pd.Series()

matching(ledger,bank_no_nsf,"Item_sep","Description_sep")

print(bank_no_nsf)
print(ledger)
