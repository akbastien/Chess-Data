#Final model
#TAKES 1-2 HOURS TO RUN

seed = 67

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold, GridSearchCV
from sklearn.metrics import balanced_accuracy_score
import warnings
warnings.filterwarnings('ignore')


pd.set_option('display.max_rows', None)


#LOAD AND PREP DATAFRAMES

dropTies = True
dropFirstMoves = True
numMoves = 10

df_train = pd.read_csv(r"C:\Users\akbas\Desktop\MATH 495\Chess Analysis\Dataframes\FinalModelTrain.csv")
df_test = pd.read_csv(r"C:\Users\akbas\Desktop\MATH 495\Chess Analysis\Dataframes\FinalModelTest.csv")


if dropTies == True:
    df_train = df_train[df_train['Winner'] != 0].reset_index(drop=True)
    df_test = df_test[df_test['Winner'] != 0].reset_index(drop=True)
if dropFirstMoves == True:
    df_train = df_train[df_train['Position No'] > numMoves].reset_index(drop=True)
    df_test = df_test[df_test['Position No'] > numMoves].reset_index(drop = True)

df_test = df_test.groupby('Game No').sample(n=1, random_state=seed).reset_index(drop=True)


X_train = df_train.drop(columns=['Game No', 'Total Positions', 'Board Vector', 'Winner'])
y_train = df_train['Winner']

X_test = df_test.drop(columns=['Game No', 'Total Positions', 'Board Vector', 'Winner'])
y_test = df_test['Winner']





#RANDOM FOREST


# Perform Cross Validation
param_grid = {
    "n_estimators": [300],
    "max_depth": [None, 10, 20],
    "min_samples_leaf": [1, 5, 20],
    "max_features": ["sqrt", 0.3],
}

if dropTies == True:
    search = GridSearchCV(
        RandomForestClassifier(n_estimators=300, random_state=seed, n_jobs = -1), 
        param_grid, 
        cv=GroupKFold(n_splits=5), scoring={"auc": "roc_auc", "bal_acc": "balanced_accuracy","acc": "accuracy"}, 
        refit="auc")
    
elif dropTies == False:
    search = GridSearchCV(
        RandomForestClassifier(n_estimators=300, random_state=seed, n_jobs = -1), 
        param_grid, 
        cv=GroupKFold(n_splits=5), 
        scoring={"auc": "roc_auc_ovo", "bal_acc": "balanced_accuracy", "acc": "accuracy"}, 
        refit="auc")
    
search.fit(X_train, y_train, groups=df_train["Game No"])



#OUTPUT AND FINAL EVALUATION
print("Seed = ", seed)
print("Drop Ties = ", dropTies)
if dropFirstMoves == True:
    print("Dropping first ", numMoves, "moves")


print(search.best_params_, search.best_score_)

print(search.best_estimator_.score(X_test, y_test))

best = search.best_estimator_
y_pred = best.predict(X_test)
proba = best.predict_proba(X_test)


print("Test accuracy:     ", accuracy_score(y_test, y_pred))
print("Test balanced acc.:", balanced_accuracy_score(y_test, y_pred))
if dropTies:
    print("Test AUC:          ", roc_auc_score(y_test, proba[:, 1]))
else:
    print("Test AUC:          ", roc_auc_score(y_test, proba, multi_class="ovo"))
