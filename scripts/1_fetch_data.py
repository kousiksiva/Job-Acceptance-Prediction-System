import pandas as pd

DATA_PATH = "notebooks/data/raw_job_data.csv"

df = pd.read_csv(DATA_PATH)

print("✅ Raw data loaded successfully")
print("-" * 50)

print("Dataset Shape (Rows, Columns):")
print(df.shape)

print("\nColumn Names:")
for col in df.columns:
    print(col)

print("\nFirst 5 Rows:")
print(df.head())
