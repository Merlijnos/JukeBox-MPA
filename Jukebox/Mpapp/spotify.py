import requests
import base64

CLIENT_ID = '993abde4e9c6440fb44366ff15d890cb'
CLIENT_SECRET = 'e40c42ddd5df4a879969c029d0980014'
AUTH_URL = 'https://accounts.spotify.com/api/token'

def get_auth_token():
    client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
    client_creds_b64 = base64.b64encode(client_creds.encode())
    token_data = {
        "grant_type": "client_credentials"
    }
    token_headers = {
        "Authorization": f"Basic {client_creds_b64.decode()}"
    }
    r = requests.post(AUTH_URL, data=token_data, headers=token_headers)
    data = r.json()
    return data['access_token']

def get_playlist(playlist_id, auth_token):
    auth_token = get_auth_token()
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers=headers)
    data = r.json()
    return data

def get_track(track_id, auth_token):
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    r = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers)
    data = r.json()
    return data