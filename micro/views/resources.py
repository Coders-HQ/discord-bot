import discord
from discord.ui import View, button, Button
from discord import Interaction, Embed

from classes import Resources, CEmbed

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