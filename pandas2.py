import pandas as pd

trials = [1, 2, 3, 4, 5, 6]

subj_id = [1] * 6

group = ['Control'] * 6

condition = ['Affect'] * 3 + ['Neutral'] * 3

data = {'Condition': condition, 'Subject_ID': subj_id, 'Trial': trials, 'Group': group}

df = pd.DataFrame(data)

df.head()