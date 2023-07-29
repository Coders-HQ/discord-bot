from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands

from classes.views import ModerationView, ResourcesView, RoleView, IssueListView
from classes.database import Database
from logger import logger
from static.paths import COGS_DIR
from API import app

from logging import Logger
import os, threading, asyncpg, uvicorn

# Grab token from .env file
TOKEN = os.getenv("TOKEN")


class DiscordBot(commands.Bot):
    def __init__(self, logger: Logger, *args, **kwargs):
        activity = discord.Activity(
            type=discord.ActivityType.watching, name="https://codershq.ae/"
        )
        intents = discord.Intents().all()

        # Setup logger
        self.logger = logger

        super().__init__(*args, activity=activity, intents=intents, **kwargs)

    async def setup_hook(self):
        for filename in os.listdir(COGS_DIR):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
        await self.tree.sync()  # Disable in production environment

        self.add_view(ResourcesView())
        self.add_view(ModerationView())
        self.add_view(RoleView())
        self.add_view(IssueListView())

        DSN = Database.get_dsn()
        self.loop.create_task(self.create_pool(DSN))

    async def create_pool(self, dsn):
        try:
            self.pool = await asyncpg.create_pool(dsn=dsn)
            msg = "PG connection success"
            self.logger.info(msg)
            print(msg)

        except Exception as e:
            self.pool = None
            msg = "Connection to PG failed, maybe recheck your credentials: {}"
            self.logger.error(msg.format(e))
            print(msg)

        return msg


# Init logger
logger = logger()

# Init bot
bot = DiscordBot(command_prefix="!", case_insensitive=True, logger=logger)
bot.remove_command("help")


def main():
    bot.run(TOKEN)


def start_api():
    try:
        logger.info("Starting the API")
        uvicorn.run(app=app, host="0.0.0.0")
        logger.info("The API is ready")
    except Exception as e:
        logger.error(f"The API couldn't start: {e}")


if __name__ == "__main__":
    threading.Thread(target=start_api).start()
    main()
