from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import joblib
from serpapi import GoogleSearch

app = Flask(__name__)
app.secret_key = "veritrust_2026_secure"

# Load the AI components
model = joblib.load('final_model.pkl')
tfidf = joblib.load('vectorizer.pkl')

# Credentials & Trusted Channels
USER_CRED = {"username": "lastgroup", "password": "lastgroup4"}
# Specified Channels: BBC, CNN, NDTV, Aaj Tak
TRUSTED_CHANNELS = ["bbc.com", "edition.cnn.com", "ndtv.com", "aajtak.in"]

def verify_on_web(text):
    # REPLACE 'YOUR_KEY' with your actual SerpApi Key
    API_KEY = "SerpApi_Key" 
    
    # Restrict search to specific channels
    site_query = " OR ".join([f"site:{s}" for s in TRUSTED_CHANNELS])
    query = f'"{text[:120]}" ({site_query})'
    
    search = GoogleSearch({"q": query, "api_key": API_KEY})
    results = search.get_dict()
    
    matches = []
    if "organic_results" in results:
        for r in results["organic_results"]:
            matches.append({
                "title": r.get('title'),
                "link": r.get('link'),
                "source": r.get('displayed_link', 'Verified News')
            })
    return matches

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    if data.get('u') == USER_CRED['username'] and data.get('p') == USER_CRED['password']:
        session['user'] = data['u']
        return jsonify({"status": "ok"})
    return jsonify({"status": "fail"}), 401

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('login_page'))
    return render_template('dashboard.html')

@app.route('/predict', methods=['POST'])
def predict():
    news_text = request.form.get('news_text')
    
    # 1. AI Analysis
    text_vector = tfidf.transform([news_text])
    prob_fake = model.predict_proba(text_vector)[0][1]
    
    # 2. Web Verification
    web_links = verify_on_web(news_text)
    
    # 3. Logic: If found on trusted sites, it's Authentic. Else, rely on AI.
    if len(web_links) > 0:
        verdict, color = "VERIFIED AUTHENTIC", "success"
    elif prob_fake > 0.6:
        verdict, color = "LIKELY FABRICATED", "danger"
    else:
        verdict, color = "UNVERIFIED / SUSPICIOUS", "warning"

    return jsonify({
        "verdict": verdict,
        "color": color,
        "ai_conf": f"{round((1 - prob_fake) * 100, 2)}%",
        "links": web_links[:3]
    })

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)