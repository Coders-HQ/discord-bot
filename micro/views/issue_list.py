import discord
from discord.ui import View, button, Button
from discord import Interaction

from classes import GitHub, CEmbed, Paginator

class IssueListView(View):
    def __init__(self, issues: list[str] = None, page_size: int = 5):
        # page_size is the amount of issues per page

        self.gh = GitHub()

        if issues is not None: 
            self.paginator = Paginator(issues, page_size)
        else: self.paginator = None
        self.page_size = page_size

        super().__init__(timeout=None)

    @button(
        label="Previous Page", emoji="⏪", disabled=True, custom_id="previous_button"
    )
    async def prev_page(self, interaction: Interaction, button: Button):
        req_user = interaction.message.interaction.user

        if self.paginator == None:
            # For persistent view
            self.paginator = self.get_paginator(interaction)

        if interaction.user != req_user:
            return await interaction.response.send_message(
                "Only the owner of the message can control the pagination menu!",
                ephemeral=True,
            )
        
        # Update disabled/enabled buttons
        if self.paginator.curr_page == 2: self.prev_page.disabled = True
        if self.paginator.curr_page == self.paginator.total_pages: self.next_page.disabled = True

        current_page = self.paginator.prev_page()
        if current_page is None:
            return
        emb = CEmbed(title="Issues", description='\n'.join(current_page))
        emb.set_footer(text=f"Page {self.paginator.curr_page} - {self.paginator.total_pages}")
        return await interaction.response.edit_message(
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

        if self.paginator == None:
            self.paginator = self.get_paginator(interaction)

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

    @button(
        label="Next Page",
        emoji="⏩",
        custom_id="forward_button",
    )
    async def next_page(self, interaction: Interaction, button: Button):
        req_user = interaction.message.interaction.user

        if self.paginator == None:
            # For persistent view
            self.paginator = self.get_paginator(interaction)

        if interaction.user != req_user:
            return await interaction.response.send_message(
                "Only the owner of the message can control the pagination menu!",
                ephemeral=True,
            )
        
        # Update disabled/enabled buttons
        if self.paginator.curr_page == 1: self.prev_page.disabled = False
        if self.paginator.curr_page == self.paginator.total_pages - 1: self.next_page.disabled = True

        current_page = self.paginator.next_page()
        if current_page is None:
            return
        
        emb = CEmbed(title="Issues", description='\n'.join(current_page))
        emb.set_footer(text=f"Page {self.paginator.curr_page} - {self.paginator.total_pages}")
        return await interaction.response.edit_message(
            embed=emb,
            view=self
        )

    def get_paginator(self, interaction: Interaction) -> Paginator:
        """
        !USED FOR PERSISTENT VIEW!
        Returns a Paginator object based on the current page of the interaction message
        """
        issues = []
        for issue in self.gh.list_issues():
            issues.append(f"### - [#{issue.number}]({issue.html_url}) {issue.title}")
            
        page_txt = interaction.message.embeds[0].footer.text
        curr_page = int(page_txt.split("Page ")[1].split(" - ")[0])
        paginator = Paginator(issues, self.page_size)

        paginator.curr_index = curr_page - 1
        paginator.curr_page = curr_page

        return paginator