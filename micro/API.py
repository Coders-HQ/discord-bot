from typing     import Optional
from discord    import Webhook, RequestsWebhookAdapter,embeds
from fastapi    import FastAPI
from pydantic   import BaseModel
from datetime   import datetime

import requests
from dotenv import load_dotenv
import os

load_dotenv()
WBID = os.getenv('WEBHOOKID')
WBTOKEN = os.getenv('WEBHOOKTOKEN')

class Event(BaseModel):
    title:              str
    image:              str
    date_time:          str
    duration:          int
    short_description:  str
    event_link:         str
    event_location:         str
    seats:              int


app = FastAPI()

from discord import Webhook, RequestsWebhookAdapter

def getEmbed(event:Event):
    date = datetime.strptime(event.date_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    return embeds.Embed.from_dict(
                {
                    'type'          :   'rich',
                    'title'         :   event.title,
                    'color'         :   0x00afb1,
                    'thumbnail'     : {
                        'url': event.image
                    },
                    'fields':[
                        {"name":"Description","value":event.short_description},
                        {"name":"Date","value":date.strftime("%Y-%m-%d")},
                        {"name":"Time","value":date.strftime("%H-%M")},
                        {"name":"duration","value":f'{event.duration}'},
                        {"name":"Link","value":f"[Click Here]({event.event_link})"},
                        {"name":"Event Location","value":event.event_location},
                        {"name":"Seats","value":f'{event.seats}'}
                    ]

                }
            )

@app.post("/bot/event")
async def publish_Event(event: Event):
    webhook = Webhook.partial(WBID, WBTOKEN, adapter=RequestsWebhookAdapter())
    webhook.send(embed = getEmbed(event))