# VeriTrust AI: Hybrid Fake News Detection System

VeriTrust AI is a real-time verification tool developed for the Information Technology department at Dhole Patil College of Engineering (SPPU).

## 🚀 How it Works
Unlike traditional models, this system uses a **Hybrid Headline-Consensus Logic**:
1. **ML Track:** Uses a Stacking Ensemble (Random Forest + XGBoost) for linguistic analysis.
2. **Web Track:** Uses SerpApi to verify keywords strictly within news headlines (`intitle:`).
3. **Consensus Rule:** A "Verified" status is only granted if 2 or more unique trusted domains (BBC, NDTV, etc.) report the headline.

## 🛠️ Installation
1. Clone the repo: `git clone https://github.com/srujankute/VeriTrust-AI.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python app.py`

## Demos
### LogIn Page
![LogIn Page](https://github.com/srujankute/VeriTrust-AI/blob/main/LogIn%20Page.png)
### True DashBoard
![True DashBoard](https://github.com/srujankute/netflix-dashboard-powerbi/blob/main/Executive%20Summary.png)
### False DashBoard
![False DashBoard](https://github.com/srujankute/netflix-dashboard-powerbi/blob/main/Executive%20Summary.png)
