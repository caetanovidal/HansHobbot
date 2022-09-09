import discord
import os
from dotenv import load_dotenv
from hans_hobbot_class import Hans_robot
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    intents=intents,
)

async def main():
    async with bot: 
        load_dotenv()
        await bot.add_cog(Hans_robot(bot))
        await bot.start((os.getenv("DISCORD_KEY")))

asyncio.run(main())

