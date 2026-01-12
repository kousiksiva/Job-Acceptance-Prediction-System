import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load cleaned dataset
DATA_PATH = "notebooks/data/cleaned_job_data.csv"
df = pd.read_csv(DATA_PATH)

# Identify target column safely
possible_targets = [
    col for col in df.columns
    if "place" in col.lower() or "status" in col.lower()
]

if len(possible_targets) == 0:
    raise ValueError("No target column found containing 'place' or 'status'")

target_col = possible_targets[0]
print("Target column used:", target_col)

# Split features and target
X = df.drop(columns=[target_col])
y = df[target_col]

# Encode categorical variables
X = pd.get_dummies(X, drop_first=True)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))
