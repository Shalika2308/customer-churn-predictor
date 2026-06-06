import pandas as pd

# Load dataset
df = pd.read_excel("data/telco_customer_churn.xlsx")

# Columns to remove
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

# Remove rows with invalid Total Charges
df = df.dropna()

print("\nDataset Shape After Cleaning:")
print(df.shape)

print("\nRemaining Columns:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())