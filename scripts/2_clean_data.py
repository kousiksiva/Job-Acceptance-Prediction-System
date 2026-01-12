import pandas as pd

RAW = "notebooks/data/raw_job_data.csv"
CLEAN = "notebooks/data/cleaned_job_data.csv"

df = pd.read_csv(RAW)

num_cols = df.select_dtypes(include=["int64","float64"]).columns
cat_cols = df.select_dtypes(include=["object"]).columns

for col in num_cols:
    df[col].fillna(df[col].median(), inplace=True)

for col in cat_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)
    df[col] = df[col].str.strip().str.title()

df.to_csv(CLEAN, index=False)
print("✅ Cleaned data saved")
