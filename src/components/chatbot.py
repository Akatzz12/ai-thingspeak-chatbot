import google.generativeai as genai
import pandas as pd

class Chatbot:
    def __init__(self, gemini_api_key, thingspeak_channel_id):
        self.gemini_api_key = gemini_api_key
        self.thingspeak_channel_id = thingspeak_channel_id
        self.conversation_history = []
        
        # Configure Gemini with safety settings
        genai.configure(api_key=self.gemini_api_key)
        
        # Configure for Gemini 1.5 Pro
        generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        
        # Initialize the model with Gemini 1.5 Pro
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",  # Updated model name
            generation_config=generation_config
        )

    def process_message(self, message, temperature_data):
        try:
            if temperature_data is None or temperature_data.empty:
                return "No temperature data available for analysis."
            
            # Convert field1 to numeric, handling any non-numeric values
            temperature_data['field1'] = pd.to_numeric(temperature_data['field1'], errors='coerce')
            
            # Format the temperature data
            latest_temp = temperature_data['field1'].iloc[-1]
            stats = temperature_data['field1'].describe()
            
            # Create a context-aware prompt
            prompt = f"""
            Analyze this temperature data and answer the user's question:
            - Latest temperature: {latest_temp:.2f}°C
            - Average: {stats['mean']:.2f}°C
            - Min: {stats['min']:.2f}°C
            - Max: {stats['max']:.2f}°C
            
            Question: {message}
            
            Provide a detailed analysis considering:
            1. Current temperature conditions
            2. Temperature trends
            3. Weather implications
            4. Relevant recommendations if applicable
            """
            
            # Generate response
            response = self.model.generate_content(prompt)
            return response.text if response else "Unable to generate response. Please try again."
                
        except Exception as e:
            print(f"Debug - Error details: {str(e)}")  # Debug log
            return f"Error: Unable to process the request. Please try again."