# -*- coding: utf-8 -*-
"""Credit Scoring Model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mwSA_bfPtknVikMAaa7ihdxOtaiChQP9
"""

# Step 1: Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve

# Step 2: Load Dataset
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1000, n_features=10, n_informative=6, n_redundant=2,
                           n_classes=2, random_state=42)

# Convert to DataFrame
df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(10)])

columns = [
    "annual_income",
    "current_debt",
    "credit_utilization",
    "credit_history_length",
    "num_of_credit_cards",
    "missed_payments",
    "num_of_loans",
    "loan_default_history",
    "monthly_expenses",
    "savings_balance"
]
df = pd.DataFrame(X, columns=columns)
df['target'] = y

print(df.head())

# Step 3: Data Preprocessing
X = df.drop('target', axis=1)
y = df['target']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 4: Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 5: Train Models

# Logistic Regression
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)

# Random Forest
rf = RandomForestClassifier()
rf.fit(X_train, y_train)

# Step 6: Predictions & Evaluation
models = {'Logistic Regression': log_reg, 'Random Forest': rf}

for name, model in models.items():
    print(f"\n🔍 Model: {name}")
    y_pred = model.predict(X_test)
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, y_prob)
        print("ROC-AUC Score:", auc)

# Step 7: Plot ROC Curve
plt.figure(figsize=(8,6))
for name, model in models.items():
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        plt.plot(fpr, tpr, label=f"{name} (AUC = {roc_auc_score(y_test, y_prob):.2f})")

plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve Comparison')
plt.legend()
plt.grid()
plt.show()