import discord
from discord.ui import Modal, TextInput
from discord import Interaction

from classes import GitHub
from .choose_label import ChooseLabelView

class IssueModal(Modal, title="Create/Update Issue"):
    issue_title = TextInput(
        label="Title of the issue",
        placeholder="Module x not working when clicking on y",
    )
    issue_description = TextInput(
        label="Description of the issue",
        placeholder="Type your description...",
        style=discord.TextStyle.long,
        required=False,
    )
    issue_lbls = []

    def __init__(self, title, update_num: int = None) -> None:
        if update_num:
            gh = GitHub()

            issue_title, issue_desc, self.issue_lbls = gh.get_details(update_num)
            self.issue_title.default = issue_title
            self.issue_description.default = issue_desc

        self.update_num = update_num

        super().__init__(title=title, timeout=None, custom_id="custom_id")

    async def on_submit(self, interaction: Interaction) -> None:
        if self.issue_lbls:
            await interaction.response.send_message(
                view=ChooseLabelView(
                    self.issue_title.value,
                    self.issue_description.value,
                    self.issue_lbls,
                    edit_num=self.update_num,
                ),
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                view=ChooseLabelView(
                    self.issue_title.value,
                    self.issue_description.value,
                    edit_num=self.update_num,
                ),
                ephemeral=True,
            )
