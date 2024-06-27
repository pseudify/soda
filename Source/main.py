import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json
import asyncio
import sys
from database import Database

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

TOKEN = os.getenv('TOKEN')
INTENTS = discord.Intents.all()

with open('config.json') as config_file:
    config = json.load(config_file)
    PREFIX = config['prefix']

client = commands.Bot(command_prefix=PREFIX, intents=INTENTS)

db = Database()
client.db = db

async def load_extensions():
    cogs_folder = './Source/Cogs'
    for root, _, files in os.walk(cogs_folder):
        for filename in files:
            if filename.endswith('.py'):
                cog_path = os.path.relpath(os.path.join(root, filename), start=cogs_folder).replace(os.sep, '.')
                await client.load_extension(f'Source.Cogs.{cog_path[:-3]}')

@client.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="%help")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print(f"Success: Connected to Discord as {client.user}")

async def main():
    async with client:
        await load_extensions()
        await client.start(TOKEN)

asyncio.run(main())
