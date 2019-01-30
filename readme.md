# Pavit's Bank Reconciliation Project 

Automate the process of a CSV file from bank to the financial structural ontology. The process of matching the balances in an entity's accounting records for a cash account to the corresponding information on a bank statement. The goal of this process is to ascertain the differences between the two, and to book changes to the accounting records as appropriate.

## Running the tests

run GUI by python with command

```
python3 GUI_class.py
```

Select bank input with data in /example-data/bank-flower-rose.csv

Select ledger input with data in /example-data/ledger-flower-rose.csv

Selecting Date Bank Column with 

* DATE

Selecting Date Ledger Column with 

* Date

Selecting multiple string column to combine with

* CODE
* OTHER PARTY
* TRANSACTION DETAILS

Selecting multiple string column to combine with 

* Details
* Ref
* Account

Selecting Withdrawals Bank Column with 

* MONEY OUT

Selecting Deposits Bank Column with 

* MONEY IN

Selecting Credit Ledger Column with 

* Money Out

Selecting Debit Ledger Column with 

* Money In

Selecting Balance Bank Column with 

* BALANCE

Selecting Balance Ledger Column with 

* Balance

## Authors

* **Pavit Suwansiri** - *Initial work* - [pavitsu](https://github.com/pavitsu)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
