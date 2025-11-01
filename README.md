Mood Logger

A simple mood-tracking web app built with Streamlit.
Users select a face emoji reflecting their mood, and entries are saved to Google Sheets for easy visualization and tracking.

Steps to run locally:
1. Clone repo
2. Install requirements: `pip install -r requirements.txt`
3. Set up Google Sheets API:
   - Create a Google Cloud service account with Drive + Sheets access, then share your Google Sheet with the service account email
4. Add credentials to Streamlit Secrets
5. Run locally: `streamlit run mochihealthapp.py`
