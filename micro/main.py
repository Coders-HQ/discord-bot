import discord
from discord.ext import commands
import os
from logger import logger as loggger
from dotenv import load_dotenv
import threading
import asyncio

# #Grab token from .env file
load_dotenv()
    
class CodersHQ(commands.Bot):
    def __init__(self, prefix, activity):
        """Initializes the commands.Bot subclass"""
        
        intents = discord.Intents().all()
        super().__init__(command_prefix=prefix, activity=activity, intents=intents, case_insensitive=True) # Initialize the super class (commands.Bot)
        self.remove_command('help') 
        self.logger = loggger()

        asyncio.run(self.load_cogs()) # Loads cogs using async
        
    def API(self):
        """Start the API using uvicorn (Recommended to run in a thread)"""

        try:
            self.logger.info('Starting the API')
            os.system('uvicorn API:app --reload')
            self.logger.info('the API is Ready')
        except Exception as e:
            self.logger.error('The API Couldn\'t start %s'%e)

    async def load_cogs(self):
        "Loads every cog (that ends with .py) in the cogs folder"

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}') # * REQUIRES ASYNC
                    self.logger.info(f'Loaded {filename}')
                except Exception as e:
                    self.logger.error(f'Failed to load {filename} {e}') # Log errors

if __name__ == "__main__":
    TOKEN = os.getenv('TOKEN')
    bot_instance = CodersHQ(prefix='!', activity=discord.Activity(type=discord.ActivityType.watching, name="https://codershq.ae/"))
    api_thread = threading.Thread(target=bot_instance.API)
    api_thread.start()
    bot_instance.run(TOKEN)