import discord
from discord.ui import View, button, Button, select, Select, Modal, TextInput
from discord import Interaction, Embed, Message

from classes import GitHub, CEmbed

class ChooseLabelView(View):
    def __init__(
        self,
        issue_title: str,
        issue_description: str = "",
        issue_lbls: list[str] = [],
        edit_num: int = None,
    ):
        self.gh = GitHub()
        labels = self.gh.get_all_labels()
        self.edit_num = edit_num

        super().__init__(timeout=None)

        self.select = Select(
            placeholder="Select your labels",
            max_values=len(labels),
            min_values=0,
            custom_id="label_select",
        )
        self.select.callback = self.callback
        for lbl in ["None"] + labels:
            self.select.add_option(
                label=lbl, value=lbl, default=True if lbl in issue_lbls else False
            )
        self.add_item(self.select)

        self.button = Button(
            label=f"{'Update' if edit_num else 'Create'} Issue",
            style=discord.ButtonStyle.green,
            custom_id="crup_issue_btn",
        )
        self.button.callback = lambda interaction: self.button_callback(
            interaction, issue_title, issue_description
        )
        self.add_item(self.button)

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()

    async def button_callback(self, interaction: Interaction, title: str, desc: str):
        await interaction.response.defer()

        if "None" in self.select.values:
            lbls = []
        else:
            lbls = self.select.values

        if self.edit_num:
            issue = self.gh.update_issue(self.edit_num, title, desc, lbls)
        else:
            issue = self.gh.create_issue(lbls, title, desc)
        embed = CEmbed()

        if issue:
            embed.title = "Issues"
            embed.description = f"Issue #{issue.number} {'created' if not self.edit_num else 'updated'}\n[Jump to issue]({issue.html_url})"
        else:
            embed.description = (
                "Unable to process /issue, please check your details and try again"
            )

        self.button.disabled = True
        self.select.disabled = True

        await interaction.edit_original_response(view=self)
        await interaction.followup.send(embed=embed)