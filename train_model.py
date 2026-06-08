import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

# 1. Load your dataset
# Ensure your CSV has columns 'text' and 'label' (0 for Real, 1 for Fake)
try:
    df = pd.read_csv('merged_news.csv').dropna()
except FileNotFoundError:
    print("Error: merged_news.csv not found in folder!")
    exit()

# Balance the data to prevent bias (50/50 Real/Fake)
min_size = df['label'].value_counts().min()
df = df.groupby('label').head(min_size)

# 2. Advanced TF-IDF (ngram_range 1,2 helps handle phrases and minor typos)
tfidf = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1,2))
X = tfidf.fit_transform(df['text'])
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Professional Stacking Ensemble
# We use Random Forest and XGBoost as base learners
estimators = [
    ('rf', RandomForestClassifier(n_estimators=100, max_depth=12, n_jobs=-1)),
    ('xgb', XGBClassifier(n_estimators=50, learning_rate=0.1, eval_metric='logloss'))
]
# Logistic Regression acts as the 'Final Judge'
model = StackingClassifier(estimators=estimators, final_estimator=LogisticRegression())

print("Training VeriTrust Hybrid Model... Please wait.")
model.fit(X_train, y_train)

# 4. Save the trained components
joblib.dump(model, 'final_model.pkl')
joblib.dump(tfidf, 'vectorizer.pkl')
print("--- SUCCESS: AI Model and Vectorizer have been saved! ---")