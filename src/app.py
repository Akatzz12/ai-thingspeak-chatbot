from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
from components.chatbot import Chatbot
from utils.thingspeak_helper import fetch_temperature_data

# Load environment variables
load_dotenv()

# Initialize the Streamlit app
st.title("AI Temperature Chatbot")

# Chatbot section (this part remains unchanged)
gemini_api_key = os.getenv("GEMINI_API_KEY")
thingspeak_channel_id = os.getenv("THINGSPEAK_CHANNEL_ID")
chatbot = Chatbot(gemini_api_key, thingspeak_channel_id)


if st.button("Get Temperature Data"):
    api_key = os.getenv("THINGSPEAK_API_KEY")
    channel_id = os.getenv("THINGSPEAK_CHANNEL_ID")
    temperature_data = fetch_temperature_data(channel_id, api_key)
    if not temperature_data.empty:
        st.dataframe(temperature_data)
    else:
        st.write("No temperature data found.")