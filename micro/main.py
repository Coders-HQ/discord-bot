import discord
from discord.ext import commands
import os
from logger import logger as loggger
from dotenv import load_dotenv
import API
import threading
import asyncio

#initalizing logger
logger = loggger()

#Grab token from .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

#Initialization of bot
activity = discord.Activity(type=discord.ActivityType.watching, name="https://codershq.ae/")
intents = discord.Intents().all()
client = commands.Bot(command_prefix = "!",  activity=activity, intents=intents, case_insensitive=True)
client.remove_command('help')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

def main():
    client.run(TOKEN)

def API():
    try:
        logger.info('Starting the API')
        os.system('uvicorn API:app --reload')
        logger.info('the API is Ready')
    except Exception as e:
        logger.error('The API Couldn\'t start %s'%e)

if __name__ == "__main__": 
    t2 = threading.Thread(target=API)
    t2.start()
    asyncio.run(main())
    