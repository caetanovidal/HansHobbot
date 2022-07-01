import discord
import os
from dotenv import load_dotenv
from hans_hobbot_class import Hans_hobbot_core

load_dotenv()
intents = discord.Intents.default()
client_discord = Hans_hobbot_core(intents=intents)       
client_discord.run(os.getenv('DISCORD_KEY'))