import discord
from discord.ui import View, button, Button
from discord import Interaction, Embed

from classes import GitHub, CEmbed, Paginator

class IssueListView(View):
    def __init__(self, issues: list[str] = None, page_size: int = 5):
        self.gh = GitHub()

        self.paginator = Paginator(issues, page_size)

        super().__init__(timeout=None)

    @button(
        label="Previous Page", emoji="⏪", disabled=True, custom_id="previous_button"
    )
    async def prev_page(self, interaction: Interaction, button: Button):
        req_user = interaction.message.interaction.user

        if interaction.user != req_user:
            return await interaction.response.send_message(
                "Only the owner of the message can control the pagination menu!",
                ephemeral=True,
            )

        current_page = self.paginator.prev_page()
        if current_page is None:
            return
        emb = CEmbed(title="Issues", description=current_page)
        emb.set_footer(text=f"Page {self.paginator.current_page} - {self.paginator.total_pages}")
        return await interaction.response.send_message(
            embed=emb,
            view=self
        )

    @button(
        label="Next Page",
        emoji="⏩",
        custom_id="forward_button",
    )
    async def next_page(self, interaction: Interaction, button: Button):
        req_user = interaction.message.interaction.user

        if interaction.user != req_user:
            return await interaction.response.send_message(
                "Only the owner of the message can control the pagination menu!",
                ephemeral=True,
            )
        
        current_page = self.paginator.next_page()
        if current_page is None:
            return
        
        emb = CEmbed(title="Issues", description=current_page)
        emb.set_footer(text=f"Page {self.paginator.current_page} - {self.paginator.total_pages}")
        return await interaction.response.send_message(
            embed=emb,
            view=self
        )

    @button(
        label="Exit",
        emoji="🗑️",
        style=discord.ButtonStyle.danger,
        custom_id="quit_button",
    )
    async def quit(self, interaction: Interaction, button: Button):
        req_user = interaction.message.interaction.user
        if interaction.user != req_user:
            return await interaction.response.send_message(
                "Only the owner of the message can control the pagination menu!",
                ephemeral=True,
            )

        try:
            await interaction.message.delete()
        except:
            embed = CEmbed(description="Unable to delete the interaction")
            await interaction.response.send_message(embed=embed, ephemeral=True)