import discord
from discord.ui import View, button, Button
from discord import Interaction, Embed, Message

from classes import CEmbed

class ModerationView(View):
    def __init__(self, embed_sent: Embed = None, profane_msg: Message = None):
        self.embed_sent = embed_sent
        self.profane_msg = profane_msg

        super().__init__(timeout=None)

    @button(
        label="Allow message",
        style=discord.ButtonStyle.green,
        custom_id="accept_button",
    )
    async def accept(self, interaction: Interaction, button: Button):
        if not self.embed_sent and not self.profane_msg:
            await self.setup(interaction)
        await interaction.response.defer()

        temp_embed = CEmbed(description="The message has been marked as non profane.")
        await self.embed_sent.edit(embed=temp_embed, delete_after=5, view=None)

    @button(
        label="Deny message", style=discord.ButtonStyle.red, custom_id="deny_button"
    )
    async def deny(self, interaction: Interaction, button: Button):
        extra = ""
        if not self.embed_sent and not self.profane_msg:
            await self.setup(interaction)

        await interaction.response.defer()
        try:
            if self.profane_msg:
                await self.profane_msg.delete()

        except discord.errors.NotFound:
            extra = "already"
            pass

        temp_embed = CEmbed(
            description=f"The potentially profane message has been {extra if extra else ''} deleted."
        )
        await self.embed_sent.edit(embed=temp_embed, delete_after=5, view=None)

    async def setup(self, interaction: Interaction):
        self.embed_sent = interaction.message
        embed = self.embed_sent.embeds[-1]

        link = embed.fields[-1].value.split("(")[-1][:-1]
        profane_cid, profane_mid = int(link.split("/")[-2]), int(link.split("/")[-1])

        channel = discord.utils.get(interaction.guild.channels, id=profane_cid)
        try:
            self.profane_msg = await channel.fetch_message(profane_mid)
        except discord.errors.NotFound:
            temp_embed = CEmbed(
                description="The potentially profane message has already been deleted."
            )
            await self.embed_sent.edit(embed=temp_embed, delete_after=5, view=None)