import json
import requests


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

def get_twitter_user(mensagem):
    mensagem = mensagem.replace(" ", "@")
    index_aroba = 0
    for word in mensagem:
        index_aroba += 1
        if word == "@":
            break
    return mensagem[index_aroba:]

def get_link_youtube(msg):
    msg = msg.replace(" ", ".")
    index_dot = 0
    for word in msg:
        index_dot += 1
        if word == ".":
            break
    return msg[index_dot:]
