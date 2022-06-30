from hashlib import new
import os
import requests
from dotenv import load_dotenv
from helpers import get_link_youtube

load_dotenv()

dict_user_streamkey = {}

payloadHeader = {'Accept': 'application/json', 'Content-type': 'application/json'}

def create_sala_w2g(message):
    url = get_link_youtube(message.content)
    user_id = message.author.id
    paylodJson = {"w2g_api_key": os.getenv('API_KEY_W2G'), 'share': url, 'bg_color': '#02000a', 'bg_opacity': '50'}
    
    r = requests.post("https://w2g.tv/rooms/create.json", headers=payloadHeader, json=paylodJson)
    r = r.json()
    stream_key = r['streamkey']
    
    dict_user_streamkey[user_id] = stream_key
    
    return f"https://w2g.tv/rooms/{stream_key}"

def update_room(message):
    try:
        url_video = get_link_youtube(message.content)
        streak_key = dict_user_streamkey[message.author.id]
        url_post = f"https://w2g.tv/rooms/{streak_key}/sync_update"
        payloadJson = {"w2g_api_key": os.getenv('API_KEY_W2G'),
                    "item_url": url_video}
        requests.post(url_post, headers=payloadHeader, json=payloadJson)
    except Exception as e:
        print(e)

def add_to_playlist(message):
    url_video = get_link_youtube(message.content)
    try:
        streak_key = dict_user_streamkey[message.author.id]
        url_post = f"https://w2g.tv/rooms/{streak_key}/playlists/current/playlist_items/sync_update"
        payloadJson = {"w2g_api_key": os.getenv('API_KEY_W2G'), "add_items": [{"url": url_video, "title": "Hello"}]}
        response = requests.post(url_post, headers=payloadHeader, json=payloadJson)
        print(response)
    except Exception as e:
        print(e)