import discord
from discord.ui import View, button, Button, select, Select, Modal, TextInput
from discord import Interaction, Embed, Message

from classes import GitHub, CEmbed

class IssueListView(View):
    def __init__(self, pages: list[Embed] = None):
        self.gh = GitHub()

        self.pages = pages
        self.current_page = 0

        super().__init__(timeout=None)

    @button(
        label="Previous Page", emoji="⏪", disabled=True, custom_id="previous_button"
    )
    async def prev_page(self, interaction: Interaction, button: Button):
        req_user = interaction.message.interaction.user
        if not self.pages:
            self.setup(interaction)

        if interaction.user != req_user:
            return await interaction.response.send_message(
                "Only the owner of the message can control the pagination menu!",
                ephemeral=True,
            )

        if not self.current_page < 0:
            self.prev_page.disabled = False
            self.next_page.disabled = False
            self.current_page -= 1

            if self.current_page == 0:
                self.prev_page.disabled = True

            current_page = self.pages[self.current_page]
            await interaction.response.edit_message(embed=current_page, view=self)

    @button(
        label="Next Page",
        emoji="⏩",
        custom_id="forward_button",
    )
    async def next_page(self, interaction: Interaction, button: Button):
        req_user = interaction.message.interaction.user
        if not self.pages:
            self.setup(interaction)

        if self.get_total_page(interaction) == 1:
            self.next_page.disabled = True
            await interaction.message.edit(view=self)
            return await interaction.response.send_message(
                "There is only one page", ephemeral=True
            )

        if interaction.user != req_user:
            return await interaction.response.send_message(
                "Only the owner of the message can control the pagination menu!",
                ephemeral=True,
            )

        if not self.current_page + 1 >= len(self.pages):
            self.next_page.disabled = False
            self.prev_page.disabled = False
            self.current_page += 1

            if self.current_page == len(self.pages) - 1:
                self.next_page.disabled = True

            current_page = self.pages[self.current_page]
            await interaction.response.edit_message(embed=current_page, view=self)

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

    def setup(self, interaction: Interaction):
        issue_list = self.gh.list_issues(paginate=True)
        self.pages = self.make_pages(issue_list)
        self.current_page = self.get_current_page(interaction) - 1  # For indexing
        self.total_pages = self.get_total_page(interaction)

    def make_pages(self, paginated: list[list]) -> list[Embed]:
        pages = []
        for idx, page in enumerate(paginated, start=1):
            embed = CEmbed(title="Issues")
            embed.set_footer(text=f"Page {idx} - {len(paginated)}")
            for issue in page:
                embed.add_field(
                    name=f"{issue.number}. {issue.title}",
                    value=f"{issue.html_url}",
                    inline=False,
                )

            pages.append(embed)

        return pages

    def get_current_page(self, interaction: Interaction) -> int:
        page_text = interaction.message.embeds[0].footer.text
        current_page = page_text.split(" - ")[0].split(" ")[-1]
        return int(current_page)

    def get_total_page(self, interaction: Interaction) -> int:
        page_text = interaction.message.embeds[0].footer.text
        total_page = page_text.split(" - ")[-1]
        return int(total_page)