import pandas as pd
import numpy as np

# s = pd.Series([1, 3, 5, np.nan, 6, 8])
#
# for col in s:
#     print(col)

dates = pd.date_range('20130101', periods=6)

df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))

print(df)

# print(df.tail(3))

# print(df.index)

# print(df.T)

print(df.sort_index(axis=1, ascending=False))
