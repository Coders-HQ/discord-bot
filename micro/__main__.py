from dotenv import load_dotenv
load_dotenv()

import discord
import datetime
from discord.ext import commands, tasks

from views import (
    ModerationView, 
    ResourcesView, 
    RoleView, 
    IssueListView
)
from classes import Database
from logger import logger
from static.paths import COGS_DIR
from static.constants import EVENTS_CHANNEL, NEXT_EVENT_CHANNEL, MEMBERCOUNT_CHANNEL
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

        # Setup channels

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
    
    @tasks.loop(minutes=10)
    async def update(self):
        # Update upcoming event channel
        if not self.events_channel.last_message:
            await self.next_event_channel.edit(name="No events yet...")
            return
        last_msg = self.events_channel.last_message
        day_value = last_msg.embeds[0].fields[1].value
        time_value = last_msg.embeds[0].fields[2].value
        date = datetime.datetime.strptime(f"{day_value} {time_value}", "%Y-%m-%d %H:%M")
        # if day and time are upcoming, set the channel name to the event. otherwise "No upcoming events"   
        if date > datetime.datetime.now():
            await self.next_event_channel.edit(name=last_msg.embeds[0].title)
        else:
            await self.next_event_channel.edit(name="No upcoming events...")

        # Update member count channel
        await self.membercount_ch.edit(name=f"Member Count: {len(self.users)}")


    async def on_ready(self):
        self.membercount_ch = await self.fetch_channel(MEMBERCOUNT_CHANNEL)
        self.events_channel = await self.fetch_channel(EVENTS_CHANNEL)
        self.next_event_channel = await self.fetch_channel(NEXT_EVENT_CHANNEL)
        await self.update()
        self.update.start()
        await self.membercount_ch.edit(name=f"Member Count: {len(self.users)}")


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
