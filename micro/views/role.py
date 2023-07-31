import discord
from discord.ui import View, select, Select
from discord import Interaction

from static import constants

class RoleView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @select(
        options=[
            discord.SelectOption(label=label, emoji=emoji)
            for label, emoji in constants.SELF_ROLES.items()
        ],
        max_values=11,
        min_values=1,
        placeholder="Select roles to apply",
        custom_id="self_role",
    )
    async def add_roles(self, interaction: Interaction, select: Select):
        await interaction.response.defer(ephemeral=True)
        roles = [
            discord.utils.get(interaction.guild.roles, name=role)
            for role in select.values
        ]

        await interaction.user.add_roles(*roles, reason="User requested")
        await interaction.followup.send("Roles added succesfully", ephemeral=True)