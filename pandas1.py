import pandas as pd
import os
import fnmatch

df = pd.read_excel('MLBPlayerSalaries.xlsx')
df.head()

# for file in os.listdir('.'):
#     if fnmatch.fnmatch(file, '*.txt'):
#         print(file)

df1 = pd.DataFrame({'Names': ['Andreas', 'George', 'Steve', 'Sarah', 'Joanna', 'Hanna'],
                   'Age': [21, 22, 20, 19, 18, 23]})

df2 = pd.DataFrame({'Names': ['Pete', 'Jordan', 'Gustaf', 'Sophie', 'Sally', 'Simone'],
                   'Age': [22, 21, 19, 19, 29, 21]})

df3 = pd.DataFrame({'Names': ['Ulrich', 'Donald', 'Jon', 'Jessica', 'Elisabeth', 'Diana'],
                   'Age': [21, 21, 20, 19, 19, 22]})

# df.to_excel('NamesAndAges.xlsx')

dfs = {'Group1': df1, 'Group2': df2, 'Group3': df3}

writer = pd.ExcelWriter('NamesAndAges.xlsx', engine='xlsxwriter')

for sheet_name in dfs.keys():
    dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)

writer.save()

