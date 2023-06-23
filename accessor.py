import requests 

client_id = '3a2ac80128794b96a57ceac318b0c6c5'
client_secret = '2a989d76821c4634a1a1d0375b1f3a6d'


def spotify_login():
    redirect_uri = 'http://localhost:5000/callback'
    scope = 'user-read-private user-read-email' 
    
    auth_url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"

    return auth_url


def spotify_callback(code):
    redirect_uri = 'http://localhost:5000/callback'
    auth_token_url = "https://accounts.spotify.com/api/token"

    # Exchange authorization code for access token
    auth_response = requests.post(
        auth_token_url,
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret,
        }
    )

    return auth_response.json()


def spotify_search(query,limit,access_token):
        
    url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'q': query, 'type': 'track', 'limit': limit}
    response = requests.get(url, headers=headers, params=params)

    return response


def spotify_token_refresh(refresh_token):
    token_url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
        }
    
    auth_response = requests.post(token_url, data=data)

    return auth_response