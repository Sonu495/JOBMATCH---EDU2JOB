# ==============================
# JOB ROLE PREDICTION — RANDOM FOREST
# ==============================

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# ------------------------------
# 1. LOAD DATASET
# ------------------------------
df = pd.read_csv("job_dataset.csv")

print("Dataset Shape:", df.shape)
print(df.head())

# ------------------------------
# 2. FEATURES & TARGET
# ------------------------------
X = df[["Degree", "Specialization", "CGPA"]]
y = df["JobRole"]

# ------------------------------
# 3. PREPROCESSING
# ------------------------------
categorical_features = ["Degree", "Specialization"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ],
    remainder="passthrough"
)

# ------------------------------
# 4. RANDOM FOREST PIPELINE
# ------------------------------
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    ))
])

# ------------------------------
# 5. TRAIN TEST SPLIT
# ------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ------------------------------
# 6. TRAIN MODEL
# ------------------------------
model.fit(X_train, y_train)

# ------------------------------
# 7. PREDICTIONS
# ------------------------------
y_pred = model.predict(X_test)

# ------------------------------
# 8. EVALUATION
# ------------------------------
accuracy = accuracy_score(y_test, y_pred)
print(f"\n🎯 Accuracy: {accuracy*100:.2f}%\n")

print("📋 Classification Report:")
print(classification_report(y_test, y_pred))

# ------------------------------
# 9. CONFUSION MATRIX HEATMAP
# ------------------------------
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(12,10))
sns.heatmap(cm, annot=False, cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

# ------------------------------
# 10. SAVE MODEL PIPELINE
# ------------------------------
joblib.dump(model, "model_pipeline.pkl")
print("\n✅ Random Forest Pipeline Saved as model_pipeline.pkl")