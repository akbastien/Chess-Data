# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 12:38:32 2026

@author: akbas
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.inspection import permutation_importance
from sklearn.model_selection import GroupShuffleSplit
import warnings
warnings.filterwarnings('ignore')


pd.set_option('display.max_rows', None)


df = pd.read_csv(r"C:\Users\akbas\Desktop\MATH 495\Chess Analysis\Dataframes\LaplacianData.csv")

df = df[df['Winner'] != 0].reset_index(drop=True)


X = df.drop(columns=['Game No', 'Total Positions', 'Board Vector', 'Winner'])
y= df['Winner']
groups = df['Game No']
feature_names = X.columns


gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
train_idx, test_idx = next(gss.split(X, y, groups=groups))

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]


clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)


#ACCURACY
y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
print("\nClassification Report:\n", classification_rep)


#GINI IMPORTANCE
importances = clf.feature_importances_
feature_imp_df = pd.DataFrame({'Feature': feature_names, 'Gini Importance': importances}).sort_values(
    'Gini Importance', ascending=False)
print(feature_imp_df)


#MEAN DECREASE IN ACCURACY
importances = []
initial_accuracy = accuracy_score(y_test, clf.predict(X_test))
for i in range(X.shape[1]):
    X_test_copy = X_test.copy()
    X_test_copy.iloc[:, i] = np.random.permutation(X_test_copy.iloc[:, i].values)
    shuff_accuracy = accuracy_score(y_test, clf.predict(X_test_copy))
    importances.append(initial_accuracy - shuff_accuracy)

accuracy_df = pd.DataFrame({'Feature': feature_names, 'Decrease in Accuracy': importances}).sort_values(
    'Decrease in Accuracy', ascending=False)
print(accuracy_df)



#PERMUTATION FEATURE IMPORTANCE
result = permutation_importance(
    clf, X_test, y_test, n_repeats=10, random_state=0, n_jobs=-1)
perm_imp_df = pd.DataFrame({'Feature': feature_names, 'Permutation Importance': result.importances_mean}).sort_values(
    'Permutation Importance', ascending=False)
print(perm_imp_df)
