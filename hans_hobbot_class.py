import discord
import twitter_request
from w2g_request import create_sala_w2g, add_to_playlist
import btc_request
from helpers import get_quote
import discord
from discord.ext import commands
import asyncio
import youtube_dl

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
    
class Hans_robot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def get(self, ctx, message):
        try:
            last_id = twitter_request.get_last_tweet_id(message)
            last_tweet_msg = twitter_request.get_last_tweet_msg(last_id)
            await ctx.channel.send(last_tweet_msg)
        except Exception as e:
            print(e)

    @commands.command()
    async def w2g(self, ctx, message):
        try:
            link_w2g = create_sala_w2g(message, ctx)
            await ctx.reply(link_w2g)
        except Exception as e:
            print(e) 

    @commands.command()
    async def addw2g(self, ctx, message):
        msg = add_to_playlist(message, ctx)
        await ctx.reply(msg)
    
    @commands.command()
    async def btc(self, ctx):
        try:
            msg = btc_request.request_helper()
            await ctx.reply(msg)
        except Exception as e:
            print(e)
            
    @commands.command()
    async def hello(self, ctx):
        await ctx.reply("Hello motherfucker!")

    @commands.command()
    async def inspire(self, message):
        quote = get_quote()
        await message.reply(quote)

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
