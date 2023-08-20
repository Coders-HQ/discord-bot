import discord
from discord import app_commands
from discord.ext import commands

from classes import GitHub as GitHubBackend
from views import IssueListView, IssueModal

from static import constants
from classes.colored_embed import CEmbed

from dotenv import load_dotenv

class GitHub(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.gh = GitHubBackend()

        super().__init__()

    @app_commands.command(name="list", description=constants.ISSUES_COMMANDS["list"])
    async def issue_list(self, interaction: discord.Interaction):
        await self.refresh_env()
        await interaction.response.defer()
        try:
            issues = self.gh.list_issues()
            if issues is None:
                embed = await self.unable_to_connect()
                return await interaction.followup.send(embed=embed)

            if len(issues) == 0:
                empty_embed = CEmbed(
                    description="There are no issues in this repository, yet"
                )
                return await interaction.followup.send(embed=empty_embed)

            # Format the list of issues into strings for the description
            issues_str = []

            for issue in issues:
                issues_str.append(f"### - [#{issue.number}]({issue.html_url}) {issue.title}")

            view = IssueListView(issues=issues_str, page_size=5)

            # Get the current page from the paginator
            curr_page = view.paginator.get_page()
            
            embed = CEmbed(title="Issues", description='\n'.join(curr_page))
            embed.set_footer(text=f"Page {view.paginator.curr_page} - {view.paginator.total_pages}")

            await interaction.followup.send(embed=embed, view=view)
            self.bot.logger.info(
                f"Successfully executed /issue list command for {interaction.user}"
            )

        except Exception as e:
            embed_error = CEmbed(
                description="Error in running /issue list, try again later"
            )
            await interaction.followup.send(embed=embed_error)

            self.bot.logger.error(f"Error in running /issue list command: {e}")

    @app_commands.command(name="get", description=constants.ISSUES_COMMANDS["get"])
    @app_commands.describe(num="Number of the issue to get")
    async def issue_get(self, interaction: discord.Interaction, num: int):
        await self.refresh_env()
        await interaction.response.defer()
        try:
            issue = self.gh.get_issue(num)
            if issue is None:
                embed = await self.unable_to_connect()
                return await interaction.followup.send(embed=embed)
            embed = CEmbed(title="Issue")
            if issue is False:
                embed.description = f"No issue with id={num} found"
                return await interaction.followup.send(embed=embed)

            embed.add_field(
                name=f"{issue.number} - {issue.title}",
                value=f"[Jump to the issue]({issue.html_url})",
            )
            embed.set_author(
                name=issue.user.name,
                url=issue.user.html_url,
                icon_url=issue.user.avatar_url,
            )
            embed.set_footer(
                text=f"Created at: {issue.created_at.strftime('%d-%m-%Y %I:%M %p')} ({issue.state})"
            )
            await interaction.followup.send(embed=embed)
            self.bot.logger.info(
                f"Successfully executed /issue get command for {interaction.user}"
            )

        except Exception as e:
            embed_error = CEmbed(
                description="Error in running /issue get, try again later"
            )
            await interaction.followup.send(embed=embed_error)

            self.bot.logger.error(f"Error in running /issue get command: {e}")

    @app_commands.command(
        name="create", description=constants.ISSUES_COMMANDS["create"]
    )
    async def issue_create(self, interaction: discord.Interaction):
        await self.refresh_env()
        try:
            if self.gh.authenticate():
                await interaction.response.send_modal(IssueModal(title="Create Issue"))
            else:
                embed = await self.unable_to_connect()
                await interaction.response.send_message(embed=embed)
       
        except Exception as e:
            embed_error = CEmbed(
                description="Error in running /issue create, try again later"
            )
            await interaction.response.send_message(embed=embed_error)

            self.bot.logger.error(f"Error in running /issue create command: {e}")

    @app_commands.command(
        name="update", description=constants.ISSUES_COMMANDS["update"]
    )
    @app_commands.describe(num="Number of the issue to get")
    async def issue_update(self, interaction: discord.Interaction, num: int):
        await self.refresh_env()
        try:
            if self.gh.authenticate():
                issue = self.gh.get_issue(num)
                if issue:
                    return await interaction.response.send_modal(IssueModal("Update Issue", num))
                
                embed = CEmbed(
                    title="Issues",
                    description=f"Issue with number={num} does not exist",
                )
                await interaction.response.send_message(embed=embed)

            else:
                embed = await self.unable_to_connect()
                await interaction.response.send_message(embed=embed)

        except Exception as e:
            embed_error = CEmbed(
                description="Error in running /issue update, try again later"
            )
            await interaction.followup.send(embed=embed_error)

            self.bot.logger.error(f"Error in running /issue update command: {e}")

    @app_commands.command(name="close", description=constants.ISSUES_COMMANDS["close"])
    @app_commands.describe(num="Number of the issue to get")
    async def issue_close(self, interaction: discord.Interaction, num: int):
        await interaction.response.defer()
        await self.refresh_env()
        try:
            issue = self.gh.get_issue(num)

            if issue is None:
                embed = await self.unable_to_connect()
                return await interaction.followup.send(embed=embed)

            if issue is False:
                embed = CEmbed(
                    title="Issues",
                    description=f"Issue with number={num} does not exist",
                )
                return await interaction.followup.send(embed=embed)
            
            self.gh.close_issue(num)

            embed = CEmbed(
                title="Issues",
                description=f"Issue '#{num} - {issue.title}' has been closed",
            )
            await interaction.followup.send(embed=embed)

            self.bot.logger.info(
                f"Successfully executed /issue close command for {interaction.user}"
            )

        except Exception as e:
            embed_error = CEmbed(
                description="Error in running /issue close, try again later"
            )
            await interaction.followup.send(embed=embed_error)

            self.bot.logger.error(f"Error in running /issue close command: {e}")

    async def unable_to_connect(self):
        embed = CEmbed(
            description="Error trying to connect with api.github.com, check credentials and try again later!"
        )
        self.bot.logger.info(
            f"Error trying to connect with api.github.com, check credentials and try again later!"
        )

        return embed

    async def refresh_env(self):
        load_dotenv(override=True)
        self.gh = GitHubBackend()

async def setup(bot: commands.Bot):  # async
    await bot.add_cog(GitHub(bot))
