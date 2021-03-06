import discord
import twitter_request
from w2g_request import create_sala_w2g, update_room, add_to_playlist
import btc_request
from helpers import get_twitter_user, get_quote, get_link_youtube

class Hans_hobbot_core(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
    
    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        
        if message.content.startswith('!hello'):
            await self.hello(message)
        
        if message.content.startswith('!inspire'):
            await self.inspire(message)
        
        if message.content.startswith('!get'):
            await self.get(message)

        if message.content.startswith('!w2g'):
            await self.w2g(message)
    
        if message.content.startswith('!upw2g'):
            update_room(message)

        if message.content.startswith('!addw2g'):
            add_to_playlist(message)

        if message.content.startswith('!btc'):
            await self.btc(message)

        if message.content.startswith("!help"):
            msg = """
            !get @twitterUser -> return the last tweet from that user
!inspire -> get a inspire quote
!w2g youtube/link -> create a room with the youtube link that you pass
!btc -> send a ticket with the btc value and variation
!upw2g -> must be done by the same person how create the room using !w2g, updates the room with a new video
!addw2g -> must be done by the same person how create the room using !w2g, add a new video to de queue
            """
            try:
                await message.channel.send(msg)
            except Exception as e:
                print(e)
    
    async def hello(self, message):
        await message.reply("Hello motherfucker!")
    
    async def inspire(self, message):
        quote = get_quote()
        await message.reply(quote)

    async def get(self, message):
        user_name = get_twitter_user(message.content)
        try:
            last_id = twitter_request.get_last_tweet_id(user_name)
            last_tweet_msg = twitter_request.get_last_tweet_msg(last_id)
            await message.channel.send(last_tweet_msg)
        except Exception as e:
            print(e)
               
    async def w2g(self, message):
        try:
            link_w2g = create_sala_w2g(message)
            await message.reply(link_w2g)
        except Exception as e:
            print(e) 
    
    async def btc(self, message):
        try:
            msg = btc_request.request_helper()
            await message.reply(msg)
        except Exception as e:
            print(e) 
    