import discord
from discord import Guild, Interaction, Message, TextChannel, Member, Embed
from discord.ext.commands import Context, Bot

from static.constants import MODERATION_CHANNEL, LOG_CHANNEL
from classes import CEmbed


def get_current_guild(
    obj: Interaction | Message | TextChannel | Member | Context,
) -> Guild:
    try:
        return obj.guild
    except AttributeError:
        return False


def get_extra_channel(
    channel_type: str, obj: Interaction | Message | TextChannel | Member | Context, bot: Bot
) -> TextChannel:
    guild = get_current_guild(obj)
    if not guild:
        raise TypeError(f"The given '{repr(obj)}' cannot extract guild property")
    channels = {
        "mod": MODERATION_CHANNEL,
        "log": LOG_CHANNEL,
    }

    req_channel = channels.get(channel_type)
    if not req_channel:
        raise ValueError(f"There is no requirement channel named '{channel_type}'")

    channel_obj = bot.get_channel(req_channel) # Get channel by ID
    if not channel_obj:
        raise ValueError(
            f"There are no existing channels in the server named '{req_channel}'"
        )
    return channel_obj


def prepare_resource_pages(paginated: list[list], lang: str) -> list[Embed]:
    pages = []
    for idx, page in enumerate(paginated, start=1):
        embed = CEmbed(title=lang)
        embed.set_footer(text=f"Page {idx} - {len(paginated)}")

        for d in page:
            for category, contents in d.items():
                text = ""
                if category == "Description":
                    text = contents
                    embed.add_field(name=category, value=text, inline=False)
                else:
                    for content in contents:
                        title = content.split(" - ")
                        if len(title) > 1:
                            link = title[-1]
                            name = " - ".join(title[:-1])
                            text += f"[{name}]({link})\n"
                        else:
                            link = content
                            text += f"{link}\n"
                    embed.add_field(name=category, value=text, inline=False)

        pages.append(embed)

    return pages
