def process_temperature_data(data):
    processed_data = []
    for entry in data:
        timestamp = entry['created_at']
        temperature = entry['field1']  
        processed_data.append({'timestamp': timestamp, 'temperature': temperature})
    return processed_data

def filter_data_by_time_range(processed_data, start_time, end_time):
    filtered_data = [
        entry for entry in processed_data
        if start_time <= entry['timestamp'] <= end_time
    ]
    return filtered_data

def get_temperature_at_time(processed_data, specific_time):
    # Get the temperature data for a specific time
    for entry in processed_data:
        if entry['timestamp'] == specific_time:
            return entry['temperature']
    return None