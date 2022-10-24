from hashlib import new
import os
import requests
from dotenv import load_dotenv
from helpers import get_link_youtube

load_dotenv()

dict_user_streamkey = {}

payloadHeader = {'Accept': 'application/json', 'Content-type': 'application/json'}

def create_sala_w2g(message, ctx):
    url = message
    paylodJson = {"w2g_api_key": os.getenv('API_KEY_W2G'), 'share': url, 'bg_color': '#02000a', 'bg_opacity': '50'}
    r = requests.post("https://api.w2g.tv/rooms/create.json", headers=payloadHeader, json=paylodJson)
    
    stream_key = format_json_link(r.json())
    
    user_id = ctx.author.id
    dict_user_streamkey[user_id] = stream_key
        
    return f"https://api.w2g.tv/rooms/{stream_key}"

def update_room(message):
    try:
        url_video = message
        streak_key = dict_user_streamkey[message.author.id]
        url_post = f"https://api.w2g.tv/rooms/{streak_key}/sync_update"
        payloadJson = {"w2g_api_key": os.getenv('API_KEY_W2G'),
                    "item_url": url_video}
        requests.post(url_post, headers=payloadHeader, json=payloadJson)
    except Exception as e:
        print(e)

def add_to_playlist(message, ctx):
    url_video = message
    title = ctx.message.embeds[0].title
    try:
        streak_key = dict_user_streamkey[ctx.author.id]
        url_post = f"https://api.w2g.tv/rooms/{streak_key}/playlists/current/playlist_items/sync_update"
        payloadJson = {"w2g_api_key": os.getenv('API_KEY_W2G'), "add_items": [{"url": url_video, "title": title}]}
        requests.post(url_post, headers=payloadHeader, json=payloadJson)
    except Exception as e:
        print(e)
    finally:
        return f"O video *{title}* foi adicionado na playlist com sucesso!"

def format_json_link(request):
    stream_key = request['streamkey']
    return stream_key
