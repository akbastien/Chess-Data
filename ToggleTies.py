"""
Created on Thurday Nov 12 @11:41, 2026

@author: Sao
"""
#This is where we define the labels and handle the float-to-integer conversion
DROP_TIES = True #Let there Option!

if DROP_TIES:
    df = df[df['Winner'] != 0.5].reset_index(drop=True).copy()
    df['Winner'] = df['Winner'].astype(int)     #1 = White, 0 = Black
    names = {1: 'White wins', 0: 'Black wins'}
    auc_labels = [0, 1]
    cr_target_names = [names[0], names[1]]
    white_label = 1
    multi_class_param = None
else:
    df['Winner'] = df['Winner'].map({0: 0, 0.5: 1, 1: 2})
    names = {2: 'White wins', 1: 'Tie', 0: 'Black wins'}
    auc_labels = [0, 1, 2]
    cr_target_names = [names[0], names[1], names[2]]
    white_label = 2
    multi_class_param = 'ovr'

#Since there are 3 classes in multiclass we have to grab the whole matrix. (Extracting Probability)
# Random Forest
pred_forest = forest.predict(X_test)
p_forest = forest.predict_proba(X_test)[:, 1] if DROP_TIES else forest.predict_proba(X_test)

# Logistic Regression
pred_logit = logit.predict(XL_test)
p_logit = logit.predict_proba(XL_test)[:, 1] if DROP_TIES else logit.predict_proba(XL_test)

#Evaluating metrics need to know how many classes there are. (AUC)
if DROP_TIES:
    auc_score = roc_auc_score(y_test, p)
else:
    auc_score = roc_auc_score(y_test, p, multi_class=multi_class_param, labels=auc_labels)

print(f"  Accuracy: {accuracy_score(y_test, pred):.4f}    AUC: {auc_score:.4f}")
print(classification_report(y_test, pred, labels=auc_labels, target_names=cr_target_names, zero_division=0))

#Table for Early, Middle, Late games
if DROP_TIES:
    forest_auc = roc_auc_score(y_test[m], p_forest[m])
    logit_auc = roc_auc_score(y_test[m], p_logit[m])
else:
    forest_auc = roc_auc_score(y_test[m], p_forest[m], multi_class=multi_class_param, labels=auc_labels)
    logit_auc = roc_auc_score(y_test[m], p_logit[m], multi_class=multi_class_param, labels=auc_labels)

#Stores the coefficient at index (the logistic regression equation)
if DROP_TIES:
    coef_idx = 0 
else:
    coef_idx = list(lr.classes_).index(white_label)

a = lr.coef_[coef_idx] / scaler.scale_
a0 = lr.intercept_[coef_idx] - (lr.coef_[coef_idx] * scaler.mean_ / scaler.scale_).sum()
