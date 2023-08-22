import discord
import requests
from discord import app_commands
from discord.ext import commands
from discord.utils import format_dt
from discord.app_commands import Choice

from classes import CEmbed
from views import RoleView

from static.misc import get_current_guild

import static.constants as constants


class Miscellaneous(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="chq", description=constants.USER_COMMANDS["chq"])
    @app_commands.describe(option="Words that describe CHQ")
    @app_commands.choices(
        option=[
            Choice(name=opt.title(), value=opt)
            for opt in ["who", "what", "events", "involve"]
        ]
    )
    async def chq(self, interaction: discord.Interaction, option: Choice[str]):
        try:
            options = {
                "who": constants.CHQ_WHO,
                "what": constants.CHQ_WHAT,
                "events": constants.CHQ_EVENTS,
                "involve": constants.CHQ_INVOLVE,
            }
            choice = options[option.value]

            embed = CEmbed.from_dict(choice)
            await interaction.response.send_message(embed=embed)

            self.bot.logger.error(
                f"Sent a reply on the /chq command to user <@{interaction.user}>"
            )

        except Exception as e:
            chq_error = CEmbed(description=f"Error sending response, try again later")
            await interaction.response.send_message(embed=chq_error)

            self.bot.logger.error(
                f"Error sending a reply on the !chq command to user <@{interaction.user}> | {e}"
            )

    @app_commands.command(name="count", description=constants.USER_COMMANDS["count"])
    @app_commands.guild_only()
    async def count(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            member_count = len(
                [
                    member
                    async for member in interaction.guild.fetch_members()
                    if not member.bot
                ]
            )

            count_embed = CEmbed(description=f"Member count: **{member_count}**")
            await interaction.followup.send(embed=count_embed)

            self.bot.logger.error(
                f"Executed /count successfully for <@{interaction.user}>"
            )

        except Exception as e:
            chq_error = CEmbed(
                description=f"Error in sending response, try again later"
            )
            await interaction.followup.send(embed=chq_error)

            self.bot.logger.error(f"Error sending a reply | {e}")

    @app_commands.command(name="age", description=constants.USER_COMMANDS["age"])
    @app_commands.describe(member="Member you want to see the age of, if any")
    @app_commands.guild_only()
    async def age(
        self, interaction: discord.Interaction, member: discord.Member = None
    ):
        try:
            if member is None:
                member = interaction.user

            dt_joined = format_dt(member.joined_at, "R")
            # [97, 114, 115, 97, 108, 32, 105, 115, 32, 100, 117, 109, 98]

            server = get_current_guild(interaction)
            embed = CEmbed(description=f"<@{member.id}> joined {server} {dt_joined}")
            await interaction.response.send_message(embed=embed)

        except Exception as e:

            embed_error = CEmbed(description="Error in running /age, try again later")
            await interaction.response.send_message(embed=embed_error)

            self.bot.logger.error(f"Error in running /age command: {e}")

    @app_commands.command(name="help", description=constants.USER_COMMANDS["help"])
    async def help(self, interaction: discord.Interaction):
        try:
            author = interaction.user
            admin_role = discord.utils.get(interaction.guild.roles, name="Admin")
            mod_role = discord.utils.get(interaction.guild.roles, name="Moderator")

            cmds = []
            cogs = set()
            
            for cog in self.bot.cogs:
                cogs.add(cog)
                for cmd in self.bot.get_cog(cog).walk_app_commands():
                    cmds.append((cog, cmd.name, cmd.description))

            description = ""
            for cog in cogs:
                if cog == "Listeners":
                    continue
                if (cog == "Admin" or cog == "Moderation") and (admin_role not in author.roles or mod_role not in author.roles):
                    continue
                description += f"## {cog}\n"
                for cmd in cmds:
                    if cmd[0] == cog:
                        description += f"`/{cmd[1]}` - {cmd[2]}\n"
                description += "\n"
            embed = CEmbed(title="_List of bot commands_", description=description) 

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            fail_embed = CEmbed(description="Failed to execute /help, try again later")
            await interaction.response.send_message(embed=fail_embed)

            self.bot.logger.info(f"Failed to run help command: {e}")

    @app_commands.command(name="ping", description=constants.USER_COMMANDS["ping"])
    async def ping(self, interaction: discord.Interaction):
        try:
            api_latency = requests.get("http://localhost:8000").elapsed.total_seconds() / 1000
            embed = CEmbed(
                description=f"# Pong!\n```diff\nBot latency: \n{'+' if self.bot.latency < 300 else '-'} {self.bot.latency * 1000:.0f}ms\nAPI Latecy: \n{'+' if api_latency < 300 else '-'} {api_latency * 1000:.0f}ms\n```"
            )
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            embed_error = CEmbed(description="Error in running /ping, try again later")
            await interaction.response.send_message(embed=embed_error)

            self.bot.logger.error(f"Error in running /ping command: {e}")

    @app_commands.command(
        name="self-role", description=constants.USER_COMMANDS["self-role"]
    )
    @app_commands.guild_only()
    async def self_role(self, interaction: discord.Interaction):
        try:
            view = RoleView()
            await interaction.response.send_message(view=view, ephemeral=True)

        except Exception as e:
            embed_error = CEmbed(
                description="Error in running /self-role, try again later"
            )
            await interaction.response.send_message(embed=embed_error)

            self.bot.logger.error(f"Error in running /self-role command: {e}")

    @app_commands.command(
        name="remove-role", description=constants.USER_COMMANDS["remove-role"]
    )
    @app_commands.choices(
        role=[Choice(name=name, value=name) for name in constants.SELF_ROLES.keys()]
    )
    @app_commands.guild_only()
    @app_commands.describe(role="Self role that you want to remove")
    async def remove_role(self, interaction: discord.Interaction, role: Choice[str]):
        await interaction.response.defer(ephemeral=True)
        try:
            fetched_role = discord.utils.get(interaction.guild.roles, name=role.value)
            msg = "You do not have this role"
            if fetched_role in interaction.user.roles:
                await interaction.user.remove_roles(
                    fetched_role, reason="User requested"
                )
                msg = "Role removed successfully"

            await interaction.followup.send(msg, ephemeral=True)

        except Exception as e:
            embed_error = CEmbed(
                description="Error in running /remove-role, try again later"
            )
            await interaction.followup.send(embed=embed_error, ephemeral=True)

            self.bot.logger.error(f"Error in running /remove-role command: {e}")


async def setup(bot):  # async
    await bot.add_cog(Miscellaneous(bot))
