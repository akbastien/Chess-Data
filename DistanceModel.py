"""
Created on Wednesday Nov 11 @8:02, 2026

@author: Sao
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

DATA_PATH = r"DistanceData.csv"
TEST_SIZE = 0.2
RANDOM_STATE = 42
N_TREES = 100
MIN_SAMPLES_LEAF = 1
RUN_PERMUTATION_IMPORTANCE = True
TOP_N = 25
DROP_TIES = False #(true = without ties and false = with ties)

pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)

if DATA_PATH.lower().endswith(('.xlsx', '.xls')):
    df = pd.read_excel(DATA_PATH)
else:
    df = pd.read_csv(DATA_PATH)

print("Games per Winner value in the file (1 = White won, 0.5 = tie, 0 = Black won):")
print(df.groupby('Winner')['Game No'].nunique().to_string())

winner_values = set(df['Winner'].unique())
if not winner_values <= {1, 0.5, 0}:
    raise SystemExit(f"\nSTOPPED: Winner should only contain 1, 0.5 and 0. Found: {sorted(winner_values)}")

last_positions = df[df['Position No'] == df['Total Positions']]
bare_kings_not_tie = (last_positions['NumPieces'] == 2) & (last_positions['Winner'] != 0.5)
if bare_kings_not_tie.any():
    raise SystemExit(
        f"\nSTOPPED: {bare_kings_not_tie.sum()} games end with only the two kings left but are not marked as a tie (0.5).\n"
        "The Winner column in this file is not coded 1 = White won, 0.5 = tie, 0 = Black won.")

if DROP_TIES:
    tied = df['Winner'] == 0.5
    print(f"\nIgnoring {df.loc[tied, 'Game No'].nunique()} tied games ({tied.sum()} positions).")
    df = df[~tied].reset_index(drop=True).copy()
    df['Winner'] = df['Winner'].astype(int)
    names = {1: 'White wins', 0: 'Black wins'}
    auc_labels = [0, 1]
    cr_target_names = [names[0], names[1]]
    white_label = 1
else:
    print("\nKeeping all games, including ties.")
    df['Winner'] = df['Winner'].map({0: 0, 0.5: 1, 1: 2})
    names = {2: 'White wins', 1: 'Tie', 0: 'Black wins'}
    auc_labels = [0, 1, 2]
    cr_target_names = [names[0], names[1], names[2]]
    white_label = 2

multi_class_param = None if DROP_TIES else 'ovr'
 
outcome = df['Winner'].map(names)
print("\nGames used:")
print(df.groupby(outcome)['Game No'].nunique().to_string())

n = df['Position No'] / df['Total Positions']
eig_cols = [c for c in df.columns if c.startswith('DistanceEigs') and not c.endswith('_max')]
eigs = df[eig_cols].fillna(0)

X = pd.concat([df[['Position No', 'NumPieces']], eigs], axis=1)
X_logit = eigs.mul(n, axis=0)

y = df['Winner']
groups = df['Game No']
print(f"\nPositions used: {len(df)}   Forest features: {X.shape[1]}   Logistic features: {X_logit.shape[1]}")

gss = GroupShuffleSplit(n_splits=1, test_size=TEST_SIZE, random_state=RANDOM_STATE)
train_idx, test_idx = next(gss.split(X, y, groups=groups))

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
XL_train, XL_test = X_logit.iloc[train_idx], X_logit.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
groups_test = groups.iloc[test_idx]
n_test = n.iloc[test_idx]

most_common_winner = y_train.mode()[0]
baseline_name = f"Always '{names[most_common_winner]}'"
baseline = (y_test == most_common_winner).mean()

print(f"Training: {groups.iloc[train_idx].nunique()} games, {len(train_idx)} positions")
print(f"Testing:  {groups_test.nunique()} games, {len(test_idx)} positions")

forest = RandomForestClassifier(n_estimators=N_TREES, min_samples_leaf=MIN_SAMPLES_LEAF,
                                random_state=RANDOM_STATE, n_jobs=-1)
forest.fit(X_train, y_train)
pred_forest = forest.predict(X_test)
p_forest = forest.predict_proba(X_test)[:, 1] if DROP_TIES else forest.predict_proba(X_test)

logit = make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000))
logit.fit(XL_train, y_train)
pred_logit = logit.predict(XL_test)
p_logit = logit.predict_proba(XL_test)[:, 1] if DROP_TIES else logit.predict_proba(XL_test)

def gap_over_baseline(pred, n_resamples=2000):
    per_game = pd.DataFrame({'model': pred == y_test.values,
                             'base': y_test.values == most_common_winner,
                             'positions': 1}).groupby(groups_test.values).sum()
    rng = np.random.default_rng(0)
    pick = rng.integers(0, len(per_game), size=(n_resamples, len(per_game)))
    model, base, positions = (per_game[c].to_numpy()[pick].sum(axis=1) for c in ('model', 'base', 'positions'))
    low, high = np.percentile((model - base) / positions, [2.5, 97.5])
    return accuracy_score(y_test, pred) - baseline, low, high

print("\n" + "=" * 78)
print("RESULTS ON THE TEST GAMES")
print("=" * 78)
print(f"Baseline ({baseline_name}): {baseline:.4f}")
print("AUC: 0.5 = the probabilities carry no information, 1.0 = perfect.\n")

for model_name, pred, p in (("Random forest", pred_forest, p_forest), ("Logistic regression", pred_logit, p_logit)):
    gap, low, high = gap_over_baseline(pred)
    verdict = ("better than the baseline" if low > 0 else
               "worse than the baseline" if high < 0 else
               "not clearly different from the baseline")
    
    if DROP_TIES:
        auc_score = roc_auc_score(y_test, p)
    else:
        auc_score = roc_auc_score(y_test, p, multi_class=multi_class_param, labels=auc_labels)

    print(f"{model_name}")
    print(f"  Accuracy: {accuracy_score(y_test, pred):.4f}    AUC: {auc_score:.4f}")
    print(f"  Accuracy minus baseline: {gap:+.4f}  (95% interval {low:+.4f} to {high:+.4f}) -> {verdict}")
    print("  Classification report:")
    print(classification_report(y_test, pred, labels=auc_labels, target_names=cr_target_names, zero_division=0))


stage = pd.cut(n_test, [0, 1 / 3, 2 / 3, 1], labels=['Early  (first third)', 'Middle (second third)', 'Late   (last third)'])
rows = []
for stage_name in stage.cat.categories:
    m = (stage == stage_name).values
    
    if DROP_TIES:
        forest_auc = roc_auc_score(y_test[m], p_forest[m])
        logit_auc = roc_auc_score(y_test[m], p_logit[m])
    else:
        forest_auc = roc_auc_score(y_test[m], p_forest[m], multi_class=multi_class_param, labels=auc_labels)
        logit_auc = roc_auc_score(y_test[m], p_logit[m], multi_class=multi_class_param, labels=auc_labels)

    rows.append({'Stage': stage_name,
                 'Positions': m.sum(),
                 baseline_name: (y_test[m] == most_common_winner).mean(),
                 'Forest accuracy': accuracy_score(y_test[m], pred_forest[m]),
                 'Forest AUC': forest_auc,
                 'Logistic accuracy': accuracy_score(y_test[m], pred_logit[m]),
                 'Logistic AUC': logit_auc})
print("By stage of the game:")
print(pd.DataFrame(rows).round(4).to_string(index=False))

print("\n" + "=" * 78)
print("RANDOM FOREST - FEATURE IMPORTANCE")
print("=" * 78)

feature_imp_df = pd.DataFrame({'Feature': X.columns, 'Gini Importance': forest.feature_importances_}).sort_values(
    'Gini Importance', ascending=False)
print(feature_imp_df.head(TOP_N).to_string(index=False))

def matrix_part(feature):
    for part in ('WW', 'WB', 'BB', 'BW'):
        if feature.startswith('DistanceEigs' + part):
            return part + ' block'
    return 'Full matrix' if feature.startswith('DistanceEigs') else feature

print("\nGini importance by part of the distance matrix:")
print(feature_imp_df.groupby(feature_imp_df['Feature'].map(matrix_part))['Gini Importance'].sum()
      .sort_values(ascending=False).round(4).to_string())

if RUN_PERMUTATION_IMPORTANCE:
    print("\nPermutation importance (this takes a few minutes)...")
    result = permutation_importance(forest, X_test, y_test, n_repeats=10, random_state=0)
    perm_imp_df = pd.DataFrame({'Feature': X.columns,
                                'Permutation Importance': result.importances_mean,
                                'Std': result.importances_std}).sort_values('Permutation Importance', ascending=False)
    print(perm_imp_df.head(TOP_N).to_string(index=False))

scaler, lr = logit[0], logit[-1]
if DROP_TIES:
    coef_idx = 0 
else:
    coef_idx = list(lr.classes_).index(white_label)

a = lr.coef_[coef_idx] / scaler.scale_
a0 = lr.intercept_[coef_idx] - (lr.coef_[coef_idx] * scaler.mean_ / scaler.scale_).sum()

equation_df = pd.DataFrame({'lambda_i': eig_cols,
                            'a_i': a,
                            'Standardised coefficient': lr.coef_[coef_idx]})
equation_df = equation_df.reindex(equation_df['Standardised coefficient'].abs().sort_values(ascending=False).index)

print("\n" + "=" * 78)
print("LOGISTIC REGRESSION - EXPLICIT EQUATION")
print("=" * 78)
print("P(White wins) = 1 / (1 + exp(-(a0 + n * sum(a_i * lambda_i))))")
print(f"a0 = {a0:.6f}")
print(equation_df.head(TOP_N).to_string(index=False))
