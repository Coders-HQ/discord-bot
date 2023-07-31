import discord
from discord.utils import utcnow
from discord.ext import commands

from classes import (
    Database, 
    GitHub, 
    CEmbed, 
    ModerationView
)

from static.misc import get_extra_channel, get_current_guild
import static.constants as constants


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.db = Database()
        self.gh = GitHub()

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info(f"The bot {self.bot.user} have logged in")
        print(f"The bot {self.bot.user} have logged in")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            guild = get_current_guild(member)
            log_channel = get_extra_channel("log", member)
            # membercountchannel = guild.get_channel(membercountchannelid)
            # await membercountchannel.edit(name = f'Member Count: {guild.member_count}')

            muted_role = discord.utils.get(guild.roles, name="Muted")
            if muted_role:
                try:
                    if not self.bot.pool:
                        self.bot.logger.error(f"Database not configured properly")
                        muted_members = []
                    else:
                        async with self.bot.pool.acquire() as connection:
                            async with connection.transaction():
                                muted_members = await self.db.get_all_muted_role(
                                    self.bot.pool
                                )

                except Exception as e:
                    self.bot.logger.error(
                        f"Error in checking muted role on user join: {e}"
                    )
                    muted_members = []

                if str(member.id) in muted_members:
                    await member.add_roles(
                        muted_role, reason="Muted member left server and rejoined"
                    )
                else:
                    await member.send(constants.CHQ_WELCOME_MESSAGE)

            else:
                await member.send(constants.CHQ_WELCOME_MESSAGE)

            log_embed = CEmbed(
                title="Member Joined",
                description=f"<@{member.id}> **({member.id})** has joined the server.",
            )
            log_embed.set_author(
                name=f"{member}", icon_url=f"{member.display_avatar.url}"
            )
            log_embed.set_footer(text=f"Member Count: {guild.member_count}")
            log_embed.timestamp = utcnow()
            await log_channel.send(embed=log_embed)

            # Logging
            self.bot.logger.info(
                f"New User: {member} ({member.id}) | Welcome Message sent, logged"
            )

        except Exception as e:
            self.bot.logger.error(
                f"Error in running on_member_join event for {member}: {e}"
            )

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        try:
            guild = member.guild
            log_channel = get_extra_channel("log", member)
            log_embed = CEmbed(
                title="Member Left",
                description=f"<@{member.id}> **({member.id})** has left the server.",
            )
            log_embed.set_author(
                name=f"{member}", icon_url=f"{member.display_avatar.url}"
            )
            log_embed.set_footer(text=f"Member Count: {guild.member_count}")
            log_embed.timestamp = utcnow()
            await log_channel.send(embed=log_embed)

            self.bot.logger.info(
                f"A member has left: {member} ({member.id}) | Message has been logged"
            )

        except Exception as e:
            self.bot.logger.error(
                f"Error in logging on_member_remove {member} ({member.id}): {e}"
            )

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent):
        try:
            msg_obj = payload.cached_message
            if msg_obj:
                msg = msg_obj.content
                if not msg:  # Defer
                    return
                if msg_obj.embeds:  # Ignore if an embed is deleted
                    return

                log_channel = get_extra_channel("log", msg_obj)
                log_embed = CEmbed(title="Message Deleted")
                log_embed.set_author(
                    name=f"{msg_obj.author}",
                    icon_url=f"{msg_obj.author.display_avatar.url}",
                )
                log_embed.add_field(name="Sent Message", value=msg, inline=False)
                log_embed.add_field(
                    name="Channel", value=f"<#{msg_obj.channel.id}>", inline=False
                )
                log_embed.timestamp = utcnow()
                log_embed.set_footer(text="Micro Logs")
                await log_channel.send(embed=log_embed)

                self.bot.logger.info(
                    f"Deleted message by {msg_obj.author} ({msg_obj.author.id}) has been logged | {msg_obj.content.encode('utf-8')}"
                )

        except Exception as e:
            self.bot.logger.error(f"Error in logging on_message_remove: {e}")

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent):
        try:
            msg = payload.message_id
            c_id = payload.channel_id
            guild_id = payload.guild_id
            if not guild_id:  # Ephemeral defered msges
                return
            channel = discord.utils.get(self.bot.get_guild(guild_id).channels, id=c_id)

            if msg is None or channel is None:
                return
            try:
                msg_obj = await channel.fetch_message(msg)
            except discord.errors.NotFound:
                if msg:
                    return
            new_msg = msg_obj.content.strip()
            old_msg = (
                payload.cached_message.content.strip()
                if payload.cached_message is not None
                else "N/A"
            )
            if (
                not old_msg
            ):  # In case the defer happens, the current empty message is edited
                return
            if msg_obj.embeds:
                return
            log_channel = get_extra_channel("log", msg_obj)

            if old_msg == new_msg:  # Fixes the link embed triggering
                return

            log_embed = CEmbed(title="Modified Message")
            log_embed.set_author(
                name=f"{msg_obj.author}",
                icon_url=f"{msg_obj.author.display_avatar.url}",
            )
            log_embed.add_field(
                name="Original Message",
                value=old_msg,
                inline=False,
            )
            log_embed.add_field(name="Modified Message", value=new_msg, inline=False)
            log_embed.add_field(name="Channel", value=channel.name, inline=False)
            log_embed.timestamp = utcnow()
            log_embed.set_footer(text="Micro Logs")
            await log_channel.send(embed=log_embed)

            self.bot.logger.info(
                f"The modified message from [{old_msg.encode('utf-8')}] to [{new_msg.encode('utf-8')}] was logged | User: {msg_obj.author}"
            )

        except Exception as e:
            self.bot.logger.error(f"Unable to execute on_raw_message_edit: {e}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            # ignore it if it's from the bot
            if message.author == self.bot.user:
                return

            # prepare the message into list of words
            msg = message.content.lower().strip().replace("\n", " ").split(" ")

            if not msg:  # If list is empty - []
                return

            elif message.content == "F":
                await message.channel.send("Respekt :3")

            if self.gh.validate_link(message.content):
                if "`" in message.content or "```" in message.content:
                    return

                code_info = self.gh.get_code_block(message.content)
                code_block = "\n".join(code_info[0])
                info_str = code_info[1][0]
                lang = code_info[1][1]
                reference = message.reference

                if code_block:
                    code_msg = "> {}\n{}\n```{}\n{}```"
                    await message.channel.send(
                        code_msg.format(message.content, info_str, lang, code_block),
                        suppress_embeds=True,
                        reference=reference,
                    )

                    await message.delete()

        except Exception as e:
            self.bot.logger.error(f"Error on running on_message: {e}")

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        try:
            muted_role = discord.utils.get(before.guild.roles, name="Muted")
            # everyone_role = discord.utils.get(before.guild.roles,name="@everyone")

            if after.roles == before.roles:
                return

            if muted_role in after.roles:
                async with self.bot.pool.acquire() as connection:
                    async with connection.transaction():
                        await self.db.add_muted_role(str(after.id), self.bot.pool)

                self.bot.logger.info(
                    f"Added muted role on database for {before.name} ({before.id})"
                )

            elif muted_role not in after.roles:
                async with self.bot.pool.acquire() as connection:
                    async with connection.transaction():
                        await self.db.remove_muted_role(str(after.id), self.bot.pool)
                self.bot.logger.info(
                    f"Removed muted role on database for {before.name} ({before.id})"
                )

        except Exception as e:
            self.bot.logger.info(
                f"Unable to update muted role on database for {before.name} ({before.id}): {e}"
            )

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.Member):
        self.bot.logger.info(
            f"User: <@{user.id}> ({user.name}) has been banned from the {guild.name}"
        )

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.Member):
        self.bot.logger.info(
            f"User: <@{user.id}> ({user.name}) has been unbanned from the {guild.name}"
        )


async def setup(bot):
    await bot.add_cog(Events(bot))  # await this
