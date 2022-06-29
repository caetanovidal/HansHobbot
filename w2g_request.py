from hashlib import new
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def create_sala_w2g(url):
    payload = {'Accept': 'application/json', 'Content-type': 'application/json'}
    paylod2 = {"w2g_api_key": os.getenv('API_KEY_W2G'), 'share': url, 'bg_color': '#02000a', 'bg_opacity': '50'}
    
    r = requests.post("https://w2g.tv/rooms/create.json", headers=payload, json=paylod2)
    r = r.json()
    stream_key = r['streamkey']
    return f"https://w2g.tv/rooms/{stream_key}"

