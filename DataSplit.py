# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 12:31:55 2026

@author: akbas
"""

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

df = pd.read_csv(r"C:/Users/akbas/Desktop/MATH 495/Chess Analysis/EigenvalueDF.csv")

# df has one row per (game, state); 'Game No' identifies the game
gss = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
train_idx, test_idx = next(gss.split(df, groups=df["Game No"]))

train_df = df.iloc[train_idx]
test_df = df.iloc[test_idx]

# sanity check: no game appears in both sets
assert set(train_df["Game No"]).isdisjoint(test_df["Game No"])


train_df.to_csv(r'C:\Users\akbas\Desktop\MATH 495\Chess Analysis\TrainData.csv', index=False)
test_df.to_csv(r'C:\Users\akbas\Desktop\MATH 495\Chess Analysis\TestData.csv', index=False)