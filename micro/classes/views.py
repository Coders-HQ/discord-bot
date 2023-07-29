import discord
from discord.ui import View, button, Button, select, Select, Modal, TextInput
from discord import Interaction, Embed, Message

from classes.resources import Resources
from classes.github import GitHub
from classes.colored_embed import CEmbed
from static import constants


class ResourcesView(View):
    def __init__(self, pages: list[Embed] = None, lang: str = None):
        self.res = Resources()

        self.pages = pages
        self.lang = lang
        self.current_page = 0

        self.res.reload_resource()
        super().__init__(timeout=None)

    @button(
        label="Previous Page", emoji="⏪", disabled=True, custom_id="button_previous"
    )
    async def prev_page(self, interaction: Interaction, button: Button):
        if not self.pages:
            self.setup(interaction)

        req_user = interaction.message.interaction.user
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

    @button(label="Next Page", emoji="⏩", custom_id="button_forward")
    async def next_page(self, interaction: Interaction, button: Button):
        if not self.pages:
            self.setup(interaction)

        if self.get_total_page(interaction) == 1:
            self.next_page.disabled = True
            await interaction.message.edit(view=self)
            return await interaction.response.send_message(
                "There is only one page", ephemeral=True
            )

        req_user = interaction.message.interaction.user

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
        custom_id="button_quit",
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

    def get_paginated(self, interaction: Interaction) -> list[list]:
        lang = self.get_lang(interaction)
        data = self.res.get_details(lang)
        paginated = self.res.prepare_pagination(data)
        return paginated

    def create_pages(self, paginated: list[list], lang: str) -> list[Embed]:
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

    def get_lang(self, interaction: Interaction) -> str:
        lang = interaction.message.embeds[0].title
        return lang

    def get_current_page(self, interaction: Interaction) -> int:
        page_text = interaction.message.embeds[0].footer.text
        current_page = page_text.split(" - ")[0].split(" ")[-1]
        return int(current_page)

    def get_total_page(self, interaction: Interaction) -> int:
        page_text = interaction.message.embeds[0].footer.text
        total_page = page_text.split(" - ")[-1]
        return int(total_page)

    def setup(self, interaction: Interaction):
        lang = self.get_lang(interaction)
        paginated = self.get_paginated(interaction)
        self.pages = self.create_pages(paginated, lang)
        current_page = self.get_current_page(interaction)
        self.total_page = self.get_total_page(interaction)
        self.current_page = current_page - 1  # Indexing


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

        temp_embed = CEmbed(description=f"The message has been marked as non profane.")
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
                description=f"The potentially profane message has already been deleted."
            )
            await self.embed_sent.edit(embed=temp_embed, delete_after=5, view=None)


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
