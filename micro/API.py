from discord import Webhook
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from classes.colored_embed import CEmbed

import os, aiohttp

class Event(BaseModel):
    title: str
    image: str
    date_time: str
    duration: int
    short_description: str
    event_link: str
    event_location: str
    seats: int


app = FastAPI()


def get_embed(event: Event):
    date = datetime.strptime(event.date_time, "%Y-%m-%d")
    return CEmbed.from_dict(
        {
            "title": event.title,
            "image": {'url': event.image},
            "fields": [
                {
                    "name": "Description", 
                    "value": event.short_description
                },

                {
                    "name": "Date",
                    "value": date.strftime("%Y-%m-%d"), 
                    "inline": True
                },
                {
                    "name": "Time",
                    "value": date.strftime("%H-%M"),
                    "inline": True
                },
                {
                    "name": "Duration",
                    "value": event.duration,
                    "inline": True
                },
                {
                    "name": "Link",
                    "value": f"[Click Here]({event.event_link})",
                    "inline": True
                },
                {
                    "name": "Event Location",
                    "value": event.event_location,
                    "inline": True
                },
                {
                    "name": "Seats",
                    "value": event.seats,
                    "inline": True
                },
            ],
        }
    )


@app.post("/bot/event")
async def publish_event(event: Event):
    WB_URL = os.getenv("WEBHOOK_URL")

    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(WB_URL, session=session)
        await webhook.send(embed=get_embed(event))
