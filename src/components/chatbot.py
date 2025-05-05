import google.generativeai as genai
import pandas as pd

class Chatbot:
    def __init__(self, gemini_api_key, thingspeak_channel_id):
        self.gemini_api_key = gemini_api_key
        self.thingspeak_channel_id = thingspeak_channel_id
        self.conversation_history = []
        
        genai.configure(api_key=self.gemini_api_key)
        
        generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",  
            generation_config=generation_config
        )

    def process_message(self, message, temperature_data):
        try:
            if temperature_data is None or temperature_data.empty:
                return "No temperature data available for analysis."
            
            temperature_data['Temperature'] = pd.to_numeric(temperature_data['Temperature'], errors='coerce')
            
            latest_temp = temperature_data['Temperature'].iloc[0]
            latest_time = temperature_data['Time (timezone)'].iloc[0]
            min_temp = temperature_data['Temperature'].min()
            min_time = temperature_data.loc[temperature_data['Temperature'].idxmin(), 'Time (timezone)']
            max_temp = temperature_data['Temperature'].max()
            max_time = temperature_data.loc[temperature_data['Temperature'].idxmax(), 'Time (timezone)']
            avg_temp = temperature_data['Temperature'].mean()
            
            time_range = (temperature_data['Time (timezone)'].max() - 
                         temperature_data['Time (timezone)'].min()).total_seconds() / 3600
            
            base_data = f"""
            Available Data:
            - Latest: {latest_temp:.2f}°C at {latest_time}
            - Minimum: {min_temp:.2f}°C at {min_time}
            - Maximum: {max_temp:.2f}°C at {max_time}
            - Average: {avg_temp:.2f}°C
            Time span: {time_range:.1f} hours ({len(temperature_data)} readings)
            """
            
            if "maximum" in message.lower() or "highest" in message.lower():
                prompt = f"""
                {base_data}
                
                Focus on analyzing the maximum temperature:
                1. State the maximum temperature and when it occurred
                2. Compare it with the average temperature
                3. Discuss any notable circumstances around this peak
                
                Conclusion: Provide a brief summary about this maximum value and its significance.
                """
            elif "minimum" in message.lower() or "lowest" in message.lower():
                prompt = f"""
                {base_data}
                
                Focus on analyzing the minimum temperature:
                1. State the minimum temperature and when it occurred
                2. Compare it with the average temperature
                3. Discuss any notable circumstances around this low point
                
                Conclusion: Provide a brief summary about this minimum value and its significance.
                """
            elif "analyze" in message.lower() or "analysis" in message.lower():
                prompt = f"""
                {base_data}
                
                Provide a comprehensive analysis:
                1. Overview of temperature range and variation
                2. Key patterns in the readings
                3. Notable changes or trends
                
                Conclusion: Summarize the key findings and highlight any areas needing attention.
                """
            else:
                prompt = f"""
                {base_data}
                
                Answer the specific question: {message}
                1. Provide a direct answer based on the data
                2. Add relevant context from available readings
                3. Note any limitations in the available data
                
                Conclusion: Summarize the key points related to this specific query.
                """
            
            response = self.model.generate_content(prompt)
            return response.text if response else "Unable to generate response. Please try again."
                
        except Exception as e:
            print(f"Debug - Error details: {str(e)}")
            return f"Error: Unable to process the request. Please try again."