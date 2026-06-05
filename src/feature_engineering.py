import pandas as pd

# =========================
# Load Dataset
# =========================

df = pd.read_excel("data/Telco_customer_churn.xlsx")

# =========================
# Data Cleaning
# =========================

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

# Convert Total Charges to numeric
df["Total Charges"] = pd.to_numeric(
    df["Total Charges"],
    errors="coerce"
)

# Remove invalid rows
df = df.dropna()

# =========================
# Derived Feature
# =========================

df["ChargesPerMonth"] = (
    df["Total Charges"] /
    (df["Tenure Months"] + 1)
)

# =========================
# Flag/Binary Feature
# =========================

df["IsLongTermCustomer"] = (
    df["Tenure Months"] > 24
).astype(int)

# =========================
# Separate Target
# =========================

y = df["Churn Value"]

X = df.drop(columns=["Churn Value"])

# =========================
# One-Hot Encoding
# =========================

categorical_columns = X.select_dtypes(
    include=["object"]
).columns

X_encoded = pd.get_dummies(
    X,
    columns=categorical_columns,
    drop_first=True
)

# =========================
# Results
# =========================

print("\n===== Feature Engineering Complete =====")

print("\nOriginal Shape:")
print(df.shape)

print("\nEncoded Shape:")
print(X_encoded.shape)

print("\nTarget Shape:")
print(y.shape)

print("\nFirst 10 Encoded Columns:")
print(X_encoded.columns[:10].tolist())

print("\nSample Data:")
print(X_encoded.head())

print("\nTarget Distribution:")
print(y.value_counts())