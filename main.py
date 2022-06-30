import discord
import os
import twitter_request
from w2g_request import create_sala_w2g, update_room, add_to_playlist
import btc_request
from helpers import get_twitter_user, get_quote, get_link_youtube
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
client_discord = discord.Client(intents=intents)

@client_discord.event
async def on_ready():
    print("We have logged in as {0.user}".format(client_discord))


@client_discord.event
async def on_message(message):
    if message.author == client_discord.user:
        return

    if message.content.startswith('$hello'):
        await message.reply('Hello motherfucker!')

    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.reply(quote)

    if message.content.startswith('!get'):
        msg = get_twitter_user(message.content)
        try:
            user_name = msg
            last_id = twitter_request.get_last_tweet_id(user_name)
            last_tweet_msg = twitter_request.get_last_tweet_msg(last_id)
            await message.channel.send(last_tweet_msg)
        except Exception as e:
            print(e)

    if message.content.startswith('!w2g'):
        try:
            link_w2g = create_sala_w2g(message)
            await message.reply(link_w2g)
        except Exception as e:
            print(e)
    
    if message.content.startswith('!upw2g'):
        update_room(message)

    if message.content.startswith('!addw2g'):
        add_to_playlist(message)

    if message.content.startswith('!btc'):
        try:
            msg = btc_request.request_helper()
            await message.reply(msg)
        except Exception as e:
            print(e)

    if message.content.startswith("!help"):
        msg = """
        !get @twitterUser -> return the last tweet from that user
$inspire -> get a inspire quote
!w2g youtube/link -> create a room with the youtube link that you pass
!btc -> send a ticket with the btc value and variation
!upw2g -> must be done by the same person how create the room using !w2g, updates the room with a new video
!addw2g -> must be done by the same person how create the room using !w2g, add a new video to de queue
        """
        try:
            await message.channel.send(msg)
        except Exception as e:
            print(e)
            
client_discord.run(os.getenv('DISCORD_KEY'))

