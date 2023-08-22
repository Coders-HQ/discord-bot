import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

from classes import Resources, CEmbed
from static import constants
from views import ResourcesView

class Programming(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.resources = Resources()

    @app_commands.command(
        name="resources", description=constants.USER_COMMANDS["resources"]
    )
    @app_commands.describe(topic="Programming language that you want the resource for")
    async def show_resources(self, interaction: discord.Interaction, topic: str):
        await interaction.response.defer()
        try:
            self.resources.reload_resource()

            req_user = interaction.user
            lang = topic
            pages = []

            data = self.resources.get_details(lang)
            paginated = self.resources.prepare_pagination(data)

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

                self.bot.logger.info(
                    f"Resource for {lang} was sent as requested by <@{req_user}>"
                )

            view = ResourcesView(pages, lang)

            await interaction.followup.send(embed=pages[view.current_page], view=view)

        except Exception as e:
            embed_error = CEmbed(
                description="Error in running /resources, try again later"
            )
            await interaction.followup.send(embed=embed_error)

            self.bot.logger.error(f"Error in running /resources command: {e}")

    @show_resources.autocomplete("topic")
    async def topic_autocomplete(self, interaction: discord.Interaction, current: str):
        self.resources.reload_resource()

        topics = self.resources.get_all_langs()
        return [
            Choice(name=lang, value=lang)
            for lang in topics
            if current.lower() in lang.lower()
        ]

async def setup(bot):  # async
    await bot.add_cog(Programming(bot))