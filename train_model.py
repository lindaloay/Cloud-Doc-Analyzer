import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
import joblib

def load_training_data(base_dir):
    texts = []
    labels = []
    for label in os.listdir(base_dir):
        label_path = os.path.join(base_dir, label)
        if os.path.isdir(label_path):
            for filename in os.listdir(label_path):
                file_path = os.path.join(label_path, filename)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                    texts.append(text)
                    labels.append(label)
    return texts, labels

# تحميل البيانات
X, y = load_training_data('training_data')

# إنشاء بايبلاين (معالجة + نموذج)
model = Pipeline([
    ('vectorizer', TfidfVectorizer(max_features=5000)),
    ('classifier', DecisionTreeClassifier())
])

# تدريب النموذج
model.fit(X, y)

# حفظ النموذج
joblib.dump(model, 'document_classifier.joblib')

print("✅ تم تدريب النموذج وحفظه بنجاح.")
