# -*- coding: utf-8 -*-
"""
Created on Thu May 13 20:57:57 2021
@summary: Expirement excel-python integration using OOP concept
@author: Shiv Muthukumar
"""

import pandas as pd

# READ EXCEL FILES INTO DATAFRAMES
df_bank = pd.read_excel(r'bank_statement.xlsx')
df_item = pd.read_excel(r'item_description.xlsx')

#print (df_bank.values.tolist())
#print (df_item.values.tolist())

# SETUP THE BANK CLASS
# THE __INIT__ PARAMETERS MUST MATCH, IN ORDER, THE COLUMNS IN EXCEL
class Bank():
    def __init__(self,bank_name,dates,orderid,desc,credit,debit,bal):
        self.bank_name = bank_name
        self.dates = dates
        self.orderid = orderid
        self.desc = desc
        self.credit = credit
        self.debit = debit
        self.bal = bal

# PREPARE A LIST TO HOLD ALL OBJECTS OF THE CLASS Bank
bank_statement_list = []

# FOR EACH ITEM FROM EXCEL, CREATE IT AS ITS OWN OBJECT
# UNIQUE ELEMENT IS GOING TO BE THE ORDERID IN THIS EXAMPLE
for each_statement in df_bank.values.tolist():
    bank_statement_list.append(Bank(*each_statement))

# LOOP OVER THE OBJECTS AND PRINT ALL THE ORDERIDS
for each_bs in bank_statement_list:
    print(each_bs.orderid)
