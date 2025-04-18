class Chatbot:
    def __init__(self, gemini_api_key, thingspeak_channel_id):
        self.gemini_api_key = gemini_api_key
        self.thingspeak_channel_id = thingspeak_channel_id

    def get_response(self, user_query):
        # Logic to interact with the Gemini API and fetch responses
        # based on the user's query regarding temperature data
        pass

    def fetch_temperature_data(self, time):
        from src.utils import thingspeak_helper
        import pandas as pd
        import os
        from dotenv import load_dotenv
        load_dotenv()
        try:
            if time:
                user_time = pd.to_datetime(time).tz_localize('UTC')
                data = thingspeak_helper.fetch_temperature_data(self.thingspeak_channel_id, os.getenv('THINGSPEAK_API_KEY'), user_time=user_time)
            else:
                data = thingspeak_helper.fetch_temperature_data(self.thingspeak_channel_id, os.getenv('THINGSPEAK_API_KEY'))
            if not data.empty:

                print(f"User Input Time: {user_time}")
                print(f"Returned Data: {data}")
                return data.to_dict('records')[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def fetch_temperature_range(self, start_time, end_time):
        # Logic to fetch temperature data from ThingSpeak
        # based on the specified time range
        pass