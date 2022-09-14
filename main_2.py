from distutils.log import error
import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

class ErrorTesting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command()
    async def test001(self, interaction):
        raise Exception('test001 app command')

    
    @app_commands.command()
    async def test002(self, interaction):
        raise Exception('test002 app command')
    
    async def cog_app_command_error(self, interaction, error) -> None:
        print('app error', type(error), error)

    
    

bot.run(os.getenv("DISCORD_TEST_NET"))