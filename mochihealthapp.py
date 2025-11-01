import streamlit as st
import pandas as pd
import json
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from streamlit_autorefresh import st_autorefresh
import plotly.express as px
import base64


st_autorefresh(interval=5000, limit=None, key="refresh")

st.title("Log a mood")

#Google authentication info
url = "https://docs.google.com/spreadsheets/d/14Qlp3YU-aLyzCsqpsbakWajG3o2JxEyOmsddZMlFW_s/edit?gid=0#gid=0"
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
key_json = base64.b64decode(st.secrets["GCP_CREDENTIALS_B64"]).decode("utf-8")
creds_dict = json.loads(key_json)
creds = Credentials.from_service_account_info(
    creds_dict,
    scopes=[
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
)

client = gspread.authorize(creds)
sheet = client.open_by_url(url).sheet1

#for resetting fields
def reset_fields():
    st.session_state["faces"] = 2
    st.session_state["text"] = ""

#create "form"
with st.form("my_form"):
    st.markdown("### How are you feeling right now?")
    sentiment_mapping = {
        0: "very sad",
        1: "sad",
        2: "neutral",
        3: "happy",
        4: "very happy",
    }
    selected = st.feedback("faces", key="faces")
    text = st.text_area("Add a note:", key="text")
    submitted = st.form_submit_button("Submit",on_click=reset_fields)
    if submitted:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([timestamp, sentiment_mapping[selected], text])
        success = st.success("✅ Added to Google Sheet!")

#read data - ideally, this would be from a database but in the interest of time we will use the sheet as a database
rows = sheet.get_all_values()
df = pd.DataFrame(rows[1:], columns=rows[0])

if not df.empty:
    #for grouping data
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['date'] = pd.to_datetime(df['Timestamp'].dt.date) 
    mood_counts = df.groupby(['date', 'mood']).size().reset_index(name='count')
    
    #keep legend in order and apply color scheme
    ordered_moods = ["very sad", "sad", "neutral", "happy", "very happy"]
    colors = ["#d73027", "#fc8d59", "#fee08b", "#91cf60", "#1a9850"]
    mood_counts['mood'] = pd.Categorical(mood_counts['mood'], categories=ordered_moods, ordered=True)
    
    #visualize
    fig = px.bar(
        mood_counts,
        x="date",
        y="count",
        color="mood",
        category_orders={"mood": ordered_moods},
        color_discrete_sequence=colors,
        title="Mood Trends Over Time"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Count",
        bargap=0.2,
        legend_title="Mood"
    )
    
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("No mood entries yet. Fill out the form above to get started!")