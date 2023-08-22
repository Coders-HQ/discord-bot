import discord
from discord import app_commands
from discord.ext import commands

from classes import Database, CEmbed
from static.misc import get_extra_channel
import static.constants as constants

from datetime import timedelta
from dotenv import load_dotenv
import asyncio


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()

    @app_commands.command(name="kick", description=constants.ADMIN_COMMANDS["kick"])
    @app_commands.guild_only()
    @app_commands.default_permissions(kick_members=True)
    @app_commands.describe(
        member="The user to kick", reason="The reason for kicking, if any"
    )
    async def kick(
        self, interaction: discord.Interaction, member: discord.Member, reason: str = ""
    ):
        await interaction.response.defer()
        try:

            await member.kick(reason=reason)

            kick_embed = CEmbed(
                description=f"<@{member.id}> has been kicked by <@{interaction.user.id}>."
            )
            await interaction.followup.send(embed=kick_embed)

            await self.send_in_log_channel(interaction, "Kick", member, reason)

            self.bot.logger.info(
                f"{member.name} ({member.id}) was kicked by {interaction.user.name} | Reason: {reason}"
            )

        except Exception as e:
            kick_error = CEmbed(description=f"Could not kick <@{member.id}>.")
            await interaction.followup.send(embed=kick_error)

            self.bot.logger.error(
                f"Could not kick {member.name} ({member.id}) by {interaction.user} | {e}"
            )

    @app_commands.command(name="ban", description=constants.ADMIN_COMMANDS["ban"])
    @app_commands.guild_only()
    @app_commands.default_permissions(ban_members=True)
    @app_commands.describe(
        member="The member to ban",
        days="How much of their recent messages to delete, in days",
        reason="The reason for banning, if any",
    )
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        days: int = 0,
        reason: str = "",
    ):
        await interaction.response.defer()
        try:
            if days > 7:
                ban_error = CEmbed(
                    description=f"You can only delete a maximum of 7 days messages"
                )
                await interaction.followup.send(embed=ban_error)
                return

            await member.ban(reason=reason, delete_message_days=days)
            self.bot.logger.info(
                f"<{member.id}> ({member.name}) has been banned by <@{interaction.user.id}>({interaction.user.name})."
            )

            ban_embed = CEmbed(
                description=f"{member.mention} has been banned by {interaction.user.mention}."
            )
            await interaction.followup.send(embed=ban_embed)

            await self.send_in_log_channel(interaction, "Ban", member, reason)

        except Exception as e:
            ban_error = CEmbed(description=f"Could not ban <@{member.id}>.")
            await interaction.followup.send(embed=ban_error)

            self.bot.logger.error(
                f"Could not ban {member.name} ({member.id}) by {interaction.user} | {e}"
            )

    @app_commands.command(name="unban", description=constants.ADMIN_COMMANDS["unban"])
    @app_commands.guild_only()
    @app_commands.default_permissions(ban_members=True)
    @app_commands.describe(
        member="The member to unban in format 'User Name#1234'",
        reason="The reason for unbanning, if any",
    )
    async def unban(
        self, interaction: discord.Interaction, member: str, reason: str = ""
    ):
        await interaction.response.defer()
        try:
            ban_list = [items async for items in interaction.guild.bans()]
            user_name, user_discriminator = member.split("#")
            if ban_list:
                for banned_user in ban_list:
                    user = banned_user.user

                    if (user.name, user.discriminator) == (
                        user_name,
                        user_discriminator,
                    ):
                        await interaction.guild.unban(user, reason=reason)
                        self.bot.logger.info(
                            f"<{user.id}> ({user.name}) has been unbanned by <@{interaction.user.id}>({interaction.user.name})."
                        )

                        unban_embed = CEmbed(
                            description=f"{user.mention} has been unbanned."
                        )
                        await interaction.followup.send(embed=unban_embed)

                        await self.send_in_log_channel(
                            interaction, "Unban", user, reason
                        )

                    else:
                        unban_embed = CEmbed(description=f"<{member}> is not banned.")
                        await interaction.followup.send(embed=unban_embed)

            else:
                unban_embed = CEmbed(description=f"There are no banned members")
                await interaction.followup.send(embed=unban_embed)

        except Exception as e:
            unban_error = CEmbed(description=f"Could not unban <{member}>.")
            await interaction.followup.send(embed=unban_error)

            self.bot.logger.error(
                f"Could not unban {member} by {interaction.user}: {e}"
            )

    @app_commands.command(name="mute", description=constants.ADMIN_COMMANDS["mute"])
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_roles=True)
    @app_commands.describe(
        member="The member to mute", reason="The reason for muting, if any"
    )
    async def mute(
        self, interaction: discord.Interaction, member: discord.Member, reason: str = ""
    ):
        await interaction.response.defer()
        try:
            muted_role = discord.utils.get(interaction.guild.roles, name="Muted")

            if not muted_role:
                wrong_config = CEmbed(description=f"Role not configured correctly.")
                return await interaction.followup.send(embed=wrong_config)

            if not self.bot.pool:
                wrong_config = CEmbed(description=f"DB connection not configured correctly.")
                return await interaction.followup.send(embed=wrong_config)

            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    add_muted = await self.db.add_muted_role(
                        str(member.id), self.bot.pool
                    )

                    if add_muted is False:
                        if muted_role not in member.roles:
                            add_muted = await self.db.add_muted_role(
                                str(member.id), self.bot.pool
                            )
                        else:
                            muted_embed = CEmbed(
                                description=f"<@{member.id}> is already muted."
                            )
                            return await interaction.followup.send(embed=muted_embed)
                    if add_muted is None:
                        muted_embed = CEmbed(
                            description=f"Required table does not exist. Use /table-create to create."
                        )
                        return await interaction.followup.send(embed=muted_embed)

            await member.add_roles(
                muted_role, reason=reason
            )  # potential error MemberNotFound

            self.bot.logger.info(
                f"{member.name} ({member.id}) was muted by {interaction.user.name} | Reason: {reason}"
            )

            muted_embed = CEmbed(description=f"<@{member.id}> has been muted.")
            await interaction.followup.send(embed=muted_embed)

            await self.send_in_log_channel(interaction, "Mute", member, reason)

        except Exception as e:
            mute_error = CEmbed(description=f"Could not mute {member.mention}.")
            await interaction.followup.send(embed=mute_error)

            self.bot.logger.error(
                f"Could not mute {member.name} ({member.id}) by {member} | {e}"
            )

    @app_commands.command(name="unmute", description=constants.ADMIN_COMMANDS["unmute"])
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_roles=True)
    @app_commands.describe(
        member="The member to unmute", reason="The reason for unmuting, if any"
    )
    async def unmute(
        self, interaction: discord.Interaction, member: discord.Member, reason: str = ""
    ):
        await interaction.response.defer()
        try:
            muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
            if not muted_role:
                wrong_config = CEmbed(description=f"Role not configured correctly.")
                return await interaction.followup.send(embed=wrong_config)
           
            if not self.bot.pool:
                wrong_config = CEmbed(description=f"DB connection not configured correctly.")
                return await interaction.followup.send(embed=wrong_config)

            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    remove_muted = await self.db.remove_muted_role(
                        str(member.id), self.bot.pool
                    )

            if remove_muted is False:
                unmuted_embed = CEmbed(
                    description=f"<@{member.id}> is already unmuted."
                )
                return await interaction.followup.send(embed=unmuted_embed)

            if remove_muted is None:
                no_table_embed = CEmbed(
                    description=f"Required table does not exist. Use /table-create to create"
                )
                return await interaction.followup.send(embed=no_table_embed)

            await member.remove_roles(muted_role, reason=reason)
            self.bot.logger.info(
                f"{member.name} ({member.id}) was unmuted by {interaction.user.name}"
            )

            unmuted_embed = CEmbed(description=f"<@{member.id}> has been unmuted.")
            await interaction.followup.send(embed=unmuted_embed)

            await self.send_in_log_channel(interaction, "Unmute", member, reason)

        except Exception as e:
            mute_error = CEmbed(description=f"Could not unmute {member.mention}.")
            await interaction.followup.send(embed=mute_error)

            self.bot.logger.error(
                f"Could not unmute {member.name} ({member.id}) by {interaction.user} | {e}"
            )

    @app_commands.command(name="purge", description=constants.ADMIN_COMMANDS["purge"])
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.describe(
        member="The member to purge message of, if any",
        amount="Amount of messages to delete",
        reason="The reason for purging, if any",
    )
    async def purge(
        self,
        interaction: discord.Interaction,
        amount: int = 0,
        member: discord.Member = None,
        reason: str = "",
    ):
        await interaction.response.defer()
        try:
            msgs = []
            if member is None:
                await interaction.channel.purge(
                    limit=amount,
                    before=await interaction.original_response(),
                    reason=reason,
                )
                self.bot.logger.info(
                    f"{amount} {'messages' if amount > 1 else 'message'} have been purged."
                )

                purge_embed = CEmbed(description=f"{amount} messages have been purged.")
                await interaction.followup.send(embed=purge_embed)

                await self.send_in_log_channel(
                    interaction, "Purge", None, reason, amount
                )

            else:
                # print([x.content for x in await ctx.channel.history(limit=amount).flatten()])
                history_lst = [
                    message
                    async for message in interaction.channel.history(
                        before=await interaction.original_response()
                    )
                ]
                for m in history_lst:
                    if len(msgs) == amount:
                        break
                    if m.author == member:
                        msgs.append(m)

                await interaction.channel.delete_messages(msgs)
                text = f"Last {amount} {'messages' if amount > 1 else 'message'} of <@{member.id}> has been purged."
                self.bot.logger.info(text)

                purge_embed = CEmbed(description=text)
                await interaction.followup.send(embed=purge_embed)

                await self.send_in_log_channel(
                    interaction, "Purge", member, reason, amount
                )

        except Exception as e:
            purge_error = CEmbed(description=f"Could not purge messsages.")
            await interaction.followup.send(embed=purge_error)

            self.bot.logger.error(f"Could not purge messages | {e}")

    @app_commands.command(
        name="softban", description=constants.ADMIN_COMMANDS["softban"]
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.describe(
        member="The member to ban",
        days="How much of their recent messages to delete, in days",
    )
    async def softban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        days: int = 0,
        reason: str = "",
    ):
        await interaction.response.defer()
        try:
            if days > 7:
                ban_error = CEmbed(
                    description=f"You can only delete a maximum of 7 days messages"
                )
                await interaction.followup.send(embed=ban_error)
                return

            await interaction.guild.ban(
                member, reason=reason if reason else "N/A", delete_message_days=days
            )
            self.bot.logger.info(
                f"Successfully softbanned {member} by {interaction.user}"
            )

            ban_embed = CEmbed(
                description=f"<@{member.id}> has been softbanned by <@{interaction.user.id}>."
            )
            await interaction.followup.send(embed=ban_embed)

            await self.send_in_log_channel(interaction, "Softban", member, reason)

            await asyncio.sleep(60)

            await interaction.guild.unban(member, reason="Softban time over")
            self.bot.logger.info(
                f"Successfully unbanned {member} by {interaction.user} after softban time"
            )

            await self.send_in_log_channel(
                interaction, "Unban", member, "Softban time over"
            )

        except Exception as e:
            embed_error = CEmbed(description=f"Error in softbanning {member.mention}")
            await interaction.followup.send(embed=embed_error)

            self.bot.logger.error(
                f"Error in in softbanning {member} ({member.id}) by {interaction.user}: {e}"
            )

    @app_commands.command(
        name="timeout", description=constants.ADMIN_COMMANDS["timeout"]
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.describe(
        member="The member to timeout",
        minutes="How long they should be timedout for, in minutes (0 - 40320)",
        reason="The reason for timeout, if any",
    )
    async def timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: int = None,
        reason: str = "",
    ):
        await interaction.response.defer()
        try:
            if minutes is None:
                await member.timeout(None)

                timeout_embed = CEmbed(
                    description=f"Timeout removed for <@{member.id}>"
                )
                await interaction.followup.send(embed=timeout_embed)
                return

            until = timedelta(minutes=minutes)
            await member.timeout(until, reason=reason)
            self.bot.logger.info(
                f"Successfully timed out {member} for {minutes} by {interaction.user}"
            )

            timeout_embed = CEmbed(
                description=f"Timeout of {minutes} {'minutes' if minutes > 1 else 'minute'} applied to <@{member.id}>"
            )
            await interaction.followup.send(embed=timeout_embed)

            await self.send_in_log_channel(
                interaction, "Timeout", member, reason, time=minutes
            )

        except Exception as e:
            embed_error = CEmbed(
                description=f"Error in applying timeout to {member.mention} by {interaction.user.mention}"
            )
            await interaction.followup.send(embed=embed_error)

            self.bot.logger.error(
                f"Error in applying timeout to {member} ({member.id}) by {interaction.user}: {e}"
            )

    @app_commands.command(
        name="lockdown", description=constants.ADMIN_COMMANDS["lockdown"]
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.describe(
        seconds="How many seconds to slowdown the channel for (0 - 21600)"
    )
    async def lockdown(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel = None,
        seconds: int = 5,
        reason: str = "",
    ):
        await interaction.response.defer()
        try:
            if channel is None:
                channel = interaction.channel

            await channel.edit(slowmode_delay=seconds)
            self.bot.logger.info(
                f"Successfully set slowmode to #{channel.name} for {seconds} by {interaction.user}"
            )

            embed = CEmbed(
                description=f"Slowmode of {seconds} seconds added to {channel.mention}"
            )
            await interaction.followup.send(embed=embed)

            await self.send_in_log_channel(
                interaction, "Lockdown", channel, reason, time=seconds
            )

        except Exception as e:
            embed_error = CEmbed(
                description=f"Error in /lockdown on {interaction.channel.name}, try again later"
            )
            await interaction.followup.send(embed=embed_error)

            self.bot.logger.info(
                f"Error in running /lockdown command on {interaction.channel} by {interaction.user}: {e}"
            )

    @app_commands.command(
        name="table-create", description=constants.ADMIN_COMMANDS["table-create"]
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_messages=True)
    async def table_create(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            role = discord.utils.get(interaction.guild.roles, name="Muted")
            members = role.members
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    create_table = await self.db.create_table(self.bot.pool)

                    for member in members:
                        add_muted = await self.db.add_muted_role(
                            str(member.id), self.bot.pool
                        )
                        if not add_muted:
                            break

            if not create_table:
                embed = CEmbed(description="Table already exists")
                return await interaction.followup.send(embed=embed)

            embed = CEmbed(
                description="Created table successfully and added pending roles"
            )
            await interaction.followup.send(embed=embed)

            self.bot.logger.info(
                f"Successfully executed /table-create command for {interaction.user}"
            )

        except Exception as e:
            embed_error = CEmbed(
                description="Error in running /table-create, try again later"
            )
            await interaction.followup.send(embed=embed_error)

            self.bot.logger.info(
                f"Error in running /table-create command by {interaction.user}: {e}"
            )

    @app_commands.command(
        name="reconnect-db", description=constants.ADMIN_COMMANDS["reconnect-db"]
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_messages=True)
    async def reconnect(self, interaction: discord.Interaction):
        await interaction.response.defer()
        load_dotenv(override=True)

        try:
            DSN = Database.get_dsn()

            message = await self.bot.create_pool(DSN)
            await interaction.followup.send(embed=CEmbed(description=message))
            self.bot.logger.info(
                f"/reconnect command succesfully ran by {interaction.user}: {message}"
            )

        except Exception as e:
            embed_error = CEmbed(
                description="Error in running /reconnect, try again later"
            )
            await interaction.followup.send(embed=embed_error)

            self.bot.logger.error(
                f"Error in running /reconnect command by {interaction.user}: {e}"
            )

    async def send_in_log_channel(
        self,
        interaction: discord.Interaction,
        action: str,
        member: discord.Member,
        reason: str = "",
        amount: int = 0,
        time: int = 0,
    ):
        log = CEmbed(title="Moderation Embed")
        log.add_field(name="Moderator", value=interaction.user.mention, inline=True)
        if action == "Purge":
            if member:
                log.add_field(name="Offender", value=f"<@{member.id}>", inline=True)
            log.add_field(
                name="Amount",
                value=f"{amount} {'messages' if amount > 1 else 'message'}",
                inline=True,
            )

        else:
            log.add_field(name="Offender", value=member.mention, inline=True)
        if action in ("Timeout", "Lockdown"):
            log.add_field(name="Effective for", value=time, inline=True)

        log.add_field(name="Action", value=action, inline=True)
        log.add_field(name="Reason", value=reason if reason else "N/A", inline=False)

        try:
            log_channel = get_extra_channel("log", obj=interaction, bot=self.bot)
        except ValueError as e:
            fail_embed = CEmbed(description=f"Log channel not set up correctly")
            return await interaction.channel.send(embed=fail_embed)

        await log_channel.send(embed=log)


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))  # await this
