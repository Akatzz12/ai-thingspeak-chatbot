def authenticate_gemini(api_key):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    return headers

def send_request_to_gemini(endpoint, headers, payload):
    import requests
    
    response = requests.post(endpoint, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def get_gemini_response(api_key, query):
    endpoint = "https://api.gemini.com/v1/query"  
    headers = authenticate_gemini(api_key)
    payload = {
        "query": query
    }
    
    return send_request_to_gemini(endpoint, headers, payload)