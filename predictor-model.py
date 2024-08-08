import sys
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, f1_score

# Load the dataset
with open('final_dataset.json', encoding='utf-8') as f:
    data = json.load(f)

# Extract relevant features and target
def extract_features(patient):
    history = ' '.join([condition['condition'] for condition in patient['medical_history']])
    allergies = ' '.join([item if isinstance(item, str) else '' for item in patient['allergies']])
    immunizations = ' '.join([vaccine['vaccine'] for vaccine in patient['immunizations']])
    lab_results = ' '.join([test['test'] for test in patient['lab_results']])
    appointments = ' '.join([f"{appt['department']} {appt['reason']}" for appt in patient['appointments']])
    return f"{history} {allergies} {immunizations} {lab_results} {appointments}"

X = [extract_features(patient) for patient in data]
y = [patient['specialty'] for patient in data]

# Text Vectorization
vectorizer = TfidfVectorizer()

# Label Encoding for specialties
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Build the model pipeline
pipeline = Pipeline([
    ('vectorizer', vectorizer),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train the model
pipeline.fit(X_train, y_train)


# Predict specialty for new data
def predict_specialty(patient_json):
    patient_features = extract_features(patient_json)
    specialty_encoded = pipeline.predict([patient_features])[0]
    return label_encoder.inverse_transform([specialty_encoded])[0]

if __name__ == "__main__":
    import subprocess
    input_data = sys.stdin.read()
    patient_json = json.loads(input_data)
    predicted_specialty = predict_specialty(patient_json)
    print(predicted_specialty)