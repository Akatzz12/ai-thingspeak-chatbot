def fetch_temperature_data(channel_id, api_key, start_time=None, end_time=None, user_time=None):
    import requests
    import pandas as pd

    base_url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json"
    params = {
        'api_key': api_key,
        'results': 8000  
    }

    if start_time and end_time:
        params['start'] = start_time
        params['end'] = end_time

    import time
    start_time = time.time()
    response = requests.get(base_url, params=params)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time to fetch data: {elapsed_time:.4f} seconds")

    if response.status_code == 200:
        data = response.json()
        feeds = data.get('feeds', [])
        print("ThingSpeak API Response:", data)
        if feeds:
            df = pd.DataFrame(feeds)
            
            df = df.rename(columns={
                'created_at': 'Time (timezone)',
                'entry_id': 'Entry ID',
                'field1': 'Temperature'
            })
            
            df['Time (timezone)'] = pd.to_datetime(df['Time (timezone)'])
            
            df = df.sort_values(by='Time (timezone)', ascending=False)
            
            df = df.reset_index(drop=True)
            
            df = df[['Entry ID', 'Time (timezone)', 'Temperature']]
            
            if user_time is not None:
                user_time = pd.to_datetime(user_time).tz_localize('UTC')
            
            try:
                if not df.empty:
                    if user_time is not None:
                        df['time_diff'] = (df['Time (timezone)'] - user_time).dt.total_seconds().abs()
                        temperature_data = df.nsmallest(1, 'time_diff')
                        temperature_data = temperature_data.drop('time_diff', axis=1)
                    else:
                        temperature_data = df
                else:
                    temperature_data = pd.DataFrame({
                        "Entry ID": [None],
                        "Time (timezone)": [None],
                        "Temperature": [None]
                    })
            except (ValueError, TypeError, KeyError) as e:
                print(f"Error processing data: {e}")
                temperature_data = pd.DataFrame({
                    "Entry ID": [None],
                    "Time (timezone)": [None],
                    "Temperature": [None]
                })
        else:
            temperature_data = pd.DataFrame()
        return temperature_data
    else:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")