from discord import Embed

from static import constants


class CEmbed(Embed):
    def __init__(self, color=constants.BOT_COLOR, *args, **kwargs):

        super().__init__(*args, color=color, **kwargs)

    @classmethod
    def from_dict(cls, data: dict):
        color = data.get("color")
        data["color"] = color if color else constants.BOT_COLOR

        return Embed.from_dict(data)
