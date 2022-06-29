import discord
import os
import twitter_request
import w2g_request
import btc_request
from helpers import get_twitter_user, get_quote, get_link_youtube
from dotenv import load_dotenv

load_dotenv()

client_discord = discord.Client()

@client_discord.event
async def on_ready():
    print("We have logged in as {0.user}".format(client_discord))


@client_discord.event
async def on_message(message):
    if message.author == client_discord.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello motherfucker!')

    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

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
        msg = get_link_youtube(message.content)
        try:
            link = w2g_request.create_sala_w2g(msg)
            await message.channel.send(link)
        except Exception as e:
            print(e)

    if message.content.startswith('!btc'):
        msg = btc_request.request_helper()
        await message.channel.send(msg)

    if message.content.startswith("!help"):
        msg = """
        !get @twitterUser -> return the last tweet from that user
$inspire -> get a inspire quote
!w2g youtube/link -> create a room with the youtube link that you pass
!btc -> send a ticket with the btc value and variation
        """
        try:
            await message.channel.send(msg)
        except Exception as e:
            print(e)

client_discord.run(os.getenv('DISCORD_KEY'))
