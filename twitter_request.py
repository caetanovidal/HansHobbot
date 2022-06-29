from webbrowser import get
import tweepy
from random import randint
import os
from dotenv import load_dotenv
load_dotenv()


client_tweet = tweepy.Client(bearer_token=os.getenv('Bearer_Token'))
client_tweet_personal = tweepy.Client(consumer_key=os.getenv('APY_Key'),
                                      consumer_secret=os.getenv('API_Key_Secret'),
                                      access_token=os.getenv('ACCESS_TOKEN'),
                                      access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'))


def get_last_tweet_id(user_name, client_normal=client_tweet):
    usuario = client_normal.get_user(username=user_name)
    id_usuario = usuario.data.id
    tweets = client_normal.get_users_tweets(id=id_usuario)
    ultimo_tweet_id = tweets.data[0].id
    return ultimo_tweet_id


def get_last_tweet_msg(id):
    msg = client_tweet.get_tweet(id)
    mensagem = msg.data
    return mensagem['text']