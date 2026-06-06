import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

#dataset loading
df = pd.read_excel("data/telco_customer_churn.xlsx")

#data cleaning
drop_columns = [
    "CustomerID",
    "Count",
    "Country",
    "State",
    "City",
    "Zip Code",
    "Lat Long",
    "Latitude",
    "Longitude",
    "Churn Label",
    "Churn Score",
    "CLTV",
    "Churn Reason"
]

df = df.drop(columns=drop_columns)

df["Total Charges"] = pd.to_numeric(
    df["Total Charges"],
    errors="coerce"
)

df = df.dropna()

print(f"Dataset shape after cleaning: {df.shape}")

#feature engineering
#Derived Feature
df["ChargesPerMonth"] = (
    df["Total Charges"] /
    (df["Tenure Months"] + 1)
)

#Flag Feature
df["IsLongTermCustomer"] = (
    df["Tenure Months"] > 24
).astype(int)

print("Feature engineering completed")

#feature and target
y = df["Churn Value"]

X = df.drop(columns=["Churn Value"])

#one - hot encoding
categorical_columns = X.select_dtypes(
    include=["object", "string"]
).columns

X = pd.get_dummies(
    X,
    columns=categorical_columns,
    drop_first=True
)

# Convert bool → int
X = X.astype(int, errors="ignore")

print(f"Encoded dataset shape: {X.shape}")

#train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"Training samples: {X_train.shape[0]}")
print(f"Testing samples : {X_test.shape[0]}")

#logistic regression
print("\nTraining Logistic Regression")

lr_model = LogisticRegression(
    max_iter=3000
)

lr_model.fit(X_train, y_train)

lr_pred = lr_model.predict(X_test)

lr_accuracy = accuracy_score(y_test, lr_pred)
lr_precision = precision_score(y_test, lr_pred)
lr_recall = recall_score(y_test, lr_pred)
lr_f1 = f1_score(y_test, lr_pred)
lr_auc = roc_auc_score(y_test, lr_pred)

print("\nLogistic Regression ")

print(f"Accuracy : {lr_accuracy:.4f}")
print(f"Precision: {lr_precision:.4f}")
print(f"Recall   : {lr_recall:.4f}")
print(f"F1 Score : {lr_f1:.4f}")
print(f"ROC-AUC  : {lr_auc:.4f}")

#random forest
print("\nTraining Random Forest...")

rf_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)

rf_accuracy = accuracy_score(y_test, rf_pred)
rf_precision = precision_score(y_test, rf_pred)
rf_recall = recall_score(y_test, rf_pred)
rf_f1 = f1_score(y_test, rf_pred)
rf_auc = roc_auc_score(y_test, rf_pred)

print("\nRandom Forest")

print(f"Accuracy : {rf_accuracy:.4f}")
print(f"Precision: {rf_precision:.4f}")
print(f"Recall   : {rf_recall:.4f}")
print(f"F1 Score : {rf_f1:.4f}")
print(f"ROC-AUC  : {rf_auc:.4f}")

#select best model
if lr_auc >= rf_auc:
    best_model = lr_model
    model_name = "Logistic Regression"
else:
    best_model = rf_model
    model_name = "Random Forest"

print(f"\nBest Model Selected: {model_name}")

#save model
joblib.dump(
    best_model,
    "models/model.pkl"
)

joblib.dump(
    X.columns.tolist(),
    "models/columns.pkl"
)

print("\nModel saved successfully!")
print("Columns saved successfully!")
print("Training pipeline completed successfully!")