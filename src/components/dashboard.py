import streamlit as st
import os
import pandas as pd
from utils.thingspeak_helper import fetch_temperature_data

st.title("AI Temperature Chatbot Dashboard")

if st.button("Get Temperature Data"):
    api_key = os.getenv("THINGSPEAK_API_KEY")
    channel_id = os.getenv("THINGSPEAK_CHANNEL_ID")
    temperature_data = fetch_temperature_data(channel_id, api_key)
    if not temperature_data.empty:
        st.write("Temperature Data:", temperature_data)
    else:
        st.write("No temperature data found.")