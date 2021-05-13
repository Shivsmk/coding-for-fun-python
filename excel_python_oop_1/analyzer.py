# -*- coding: utf-8 -*-
"""
Created on Thu May 13 20:57:57 2021
@summary: Expirement excel-python integration using OOP concept
@author: Shiv Muthukumar
"""

import pandas as pd

df_bank = pd.read_excel(r'bank_statement.xlsx')
df_item = pd.read_excel(r'item_description.xlsx')

print (df_bank.values.tolist())
print (df_item.values.tolist())
