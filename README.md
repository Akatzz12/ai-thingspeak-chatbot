# ai-thingspeak-chatbot/ai-thingspeak-chatbot/README.md

# AI ThingSpeak Chatbot

This project is an AI-powered chatbot that interacts with the ThingSpeak API to retrieve temperature data based on user queries. The chatbot is designed to work with the Gemini 1.5 Flash API and provides a Streamlit dashboard for user interaction.

## Project Structure

```
ai-thingspeak-chatbot
├── src
│   ├── app.py                # Entry point of the application
│   ├── components
│   │   ├── chatbot.py        # Chatbot logic and interaction with Gemini API
│   │   └── dashboard.py      # Streamlit dashboard setup
│   ├── utils
│   │   ├── gemini_helper.py  # Helper functions for Gemini API
│   │   ├── thingspeak_helper.py # Functions to fetch data from ThingSpeak
│   │   └── data_processor.py  # Data processing functions
│   └── config
│       └── settings.py       # Configuration settings and environment variables
├── .env                       # Environment variables for API keys and channel ID
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ai-thingspeak-chatbot
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your API keys and channel ID:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   THINGSPEAK_API_KEY=your_thingspeak_api_key
   THINGSPEAK_CHANNEL_ID=your_channel_id
   ```

5. Run the application:
   ```
   streamlit run src/app.py
   ```

## Usage

- Open the Streamlit dashboard in your browser.
- Use the chatbot interface to ask for temperature data by specifying a time or a range of times.
- The chatbot will retrieve the requested data from ThingSpeak and provide responses based on the queries.

## Overview

This chatbot leverages the capabilities of the Gemini API to provide intelligent responses based on real-time temperature data. The Streamlit dashboard offers a user-friendly interface for interaction, making it easy to query and visualize temperature information.