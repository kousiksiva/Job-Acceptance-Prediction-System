import pandas as pd

PATH = "notebooks/data/cleaned_job_data.csv"
df = pd.read_csv(PATH)

df["experience_category"] = df["age_years"].apply(
    lambda x: "Fresher" if x < 23 else "Junior" if x <= 28 else "Senior"
)

df["skill_level"] = df["technical_score"].apply(
    lambda x: "Low" if x < 50 else "Medium" if x < 75 else "High"
)

df.to_csv(PATH, index=False)
print("✅ Feature engineering done")
