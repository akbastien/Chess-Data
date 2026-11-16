#Centrality random forest


seed = 67

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import roc_auc_score
import warnings
warnings.filterwarnings('ignore')


pd.set_option('display.max_rows', None)


df = pd.read_csv(r"C:\Users\akbas\Desktop\MATH 495\Chess Analysis\Dataframes\CentralityTrain.csv")

#df = df.groupby('Game No').sample(n=1, random_state=seed).reset_index(drop=True)
df = df[df['Winner'] != 0].reset_index(drop=True)
#df = df[df['Position No'] > 10].reset_index(drop=True)


X = df.drop(columns=['Game No', 'Total Positions', 'Board Vector', 'Winner'])
y= df['Winner']
groups = df['Game No']
#feature_names = X.columns


gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed)
train_idx, test_idx = next(gss.split(X, y, groups=groups))

X_train = X.iloc[train_idx]
#X_test = X.iloc[test_idx]
y_train= y.iloc[train_idx]
#y_test = y.iloc[test_idx]

test_df = df.iloc[test_idx].groupby('Game No').sample(n=1, random_state=seed)
X_test, y_test = X.loc[test_df.index], y.loc[test_df.index]


clf = RandomForestClassifier(n_estimators=100, random_state=seed)
clf.fit(X_train, y_train)
#

#ACCURACY
y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
print("\nClassification Report:\n", classification_rep)

#AUC
proba = clf.predict_proba(X_test)[:, 1]    # probability of class 1 (white win)
auc = roc_auc_score(y_test, proba)
print(f"AUC: {auc:.3f}")


