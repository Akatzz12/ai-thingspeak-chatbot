def fetch_temperature_data(channel_id, api_key, start_time=None, end_time=None, user_time=None):
    import requests
    import pandas as pd

    base_url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json"
    params = {
        'api_key': api_key,
        'results': 8000  # Adjust as needed
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
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_convert('UTC')
            if user_time is not None:
                user_time = pd.to_datetime(user_time).tz_localize('UTC')
            try:
                if not df.empty:
                    if user_time is not None:
                        df['time_diff'] = (df['created_at'] - user_time).dt.total_seconds().abs()
                        temperature_data = df.nsmallest(1, 'time_diff')
                    else:
                        temperature_data = df


                    
                else:
                    temperature_data = pd.DataFrame({"field1":[None],"entry_id":[None],"created_at":[None]})
            except (ValueError, TypeError, KeyError) as e:
                print(f"Error processing data: {e}")
                temperature_data = pd.DataFrame({"field1":[None],"entry_id":[None],"created_at":[None]})
        else:
            temperature_data = pd.DataFrame()
        return temperature_data
    else:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")