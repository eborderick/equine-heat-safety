# Equi-Weather Safety Metrics

A live, real-time weather analytics utility for equine thermodynamics, hosted under the Equine Analytics Hub portfolio.

This can be directly accessed by the following link: https://equi-weather-safety-metrics.streamlit.app/

## Core Features
- **Live Meteorological Sync:** Direct tracking of ambient temperature, relative humidity, wind velocity, and cloud cover indexes via OpenWeatherMap.
- **Advanced Physiological Matrix:** Algorithms mapping variables including age, breed morphology, Henneke Body Condition Score (BCS), hydration status, and endocrine pathologies (Cushing's/PPID, Anhidrosis, Equine Asthma).
- **Dynamic Risk Adjustment:** Real-time application of multi-factor risk points translating directly into actionable veterinary operational protocols.
- **Fail-Safe Manual Override:** On-demand local psychrometer telemetry entry bypassing network dependencies.

## Technical Specifications & Architecture
- **Language Stack:** Python 3.9+
- **Core Engine UI:** Streamlit Framework
- **Data Integration:** RESTful API Requests (JSON data structures)

## Installation & Local Development
To execute this web application within a local environment:

```bash
# Clone the repository
git clone [https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git)

# Navigate to directory
cd YOUR_REPO_NAME

# Install pinned production dependencies
pip install -r requirements.txt

# Launch local development server
streamlit run app.py
