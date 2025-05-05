import streamlit as st
import os
from dotenv import load_dotenv
from components.chatbot import Chatbot
from utils.thingspeak_helper import fetch_temperature_data

load_dotenv()

st.set_page_config(layout="wide")

st.markdown("""
<style>
    .chat-container {
        border: 1px solid #eee;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        height: 400px;
        overflow-y: auto;
    }
    .user-message {
        background: #e6f3ff;
        padding: 8px 12px;
        border-radius: 15px;
        margin: 5px 0;
        max-width: 80%;
        margin-left: auto;
    }
    .bot-message {
        background: #f0f0f0;
        padding: 8px 12px;
        border-radius: 15px;
        margin: 5px 0;
        max-width: 80%;
    }
</style>
""", unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'temperature_data' not in st.session_state:
    st.session_state.temperature_data = None
if 'first_load' not in st.session_state:
    st.session_state.first_load = True

col1, col2 = st.columns([0.6, 0.4])

chatbot = Chatbot(
    gemini_api_key=os.getenv("GEMINI_API_KEY"),
    thingspeak_channel_id=os.getenv("THINGSPEAK_CHANNEL_ID")
)

with col1:
    st.title("Temperature Data")
    
    if st.session_state.first_load:
        api_key = os.getenv("THINGSPEAK_API_KEY")
        channel_id = os.getenv("THINGSPEAK_CHANNEL_ID")
        temperature_data = fetch_temperature_data(channel_id, api_key)
        if not temperature_data.empty:
            st.session_state.temperature_data = temperature_data
            st.session_state.first_load = False
    
    if st.button("Refresh Data"):
        api_key = os.getenv("THINGSPEAK_API_KEY")
        channel_id = os.getenv("THINGSPEAK_CHANNEL_ID")
        temperature_data = fetch_temperature_data(channel_id, api_key)
        if not temperature_data.empty:
            st.session_state.temperature_data = temperature_data
    
    if st.session_state.temperature_data is not None:
        st.dataframe(st.session_state.temperature_data, use_container_width=True)
    else:
        st.write("No temperature data found.")

with col2:
    st.title("Chat with AI")
    
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message['type'] == 'user':
                st.markdown(f"<div class='user-message'>{message['text']}</div>", 
                          unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bot-message'>{message['text']}</div>", 
                          unsafe_allow_html=True)
    
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input("Ask about temperature data", key="user_input")
        submit_button = st.form_submit_button("Send")
        
        if submit_button and user_input:
            if st.session_state.temperature_data is None:
                st.error("Please refresh the temperature data first!")
            else:
                st.session_state.chat_history.append({
                    'type': 'user',
                    'text': user_input
                })
                
                response = chatbot.process_message(user_input, st.session_state.temperature_data)
                
                st.session_state.chat_history.append({
                    'type': 'bot',
                    'text': response
                })
                
                st.rerun()