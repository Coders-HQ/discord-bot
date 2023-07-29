import psutil
import os
import discord
from discord.ext import commands
from logger import logger as loggger
from classes.badWords import BadWords
import datetime
import static.constants as constants

log_channel_id = constants.LOG_CHANNELID
mod_channel_id = constants.MODERATION_CHANNELID
guild_id = constants.GUILD_ID
bot_color = constants.BOT_COLOR

#initalizing logger
logger = loggger()
insult = BadWords(logger)

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.process = psutil.Process(os.getpid())
        
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'The bot {self.client.user} have logged in')
        print(f'The bot {self.client.user} have logged in')
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            #Variables
            guild = member.guild
            log_channel = guild.get_channel(log_channel_id)
            muted_role = discord.utils.get(guild.roles,name="Muted")

            #Actions
            welcome_embed = discord.Embed(title="Welcome to coders (hq)", description=f"Hey there {member.name}, and welcome to coders (hq)! Before you start your journey with us there's a few things to do, check out the following channels:\n\n<#914744667176849448>\n<#910402290618368031>\n<#912986014052679701>\n\nRun !chq to know more about us and we're glad to have you in the community. We'd love to know more about you <#931237033337294889>", color=0x00afb1)
            welcome_embed.set_thumbnail(url="https://www.arsal.xyz/CHQLogo.png")
            await member.send(constants.CHQ_WELCOME_MESSAGE)
            
            log_embed = discord.Embed(title="Member Joined", description=f"<@{member.id}> **({member.id})** has joined the server.", color=bot_color)
            log_embed.set_author(name=f"{member}", icon_url=f"{member.avatar_url}")   
            log_embed.set_footer(text=f"Member Count: {guild.member_count}")
            log_embed.timestamp = datetime.datetime.utcnow()
            await log_channel.send(embed=log_embed)

            # Logging
            logger.info(f"New User: {member} ({member.id}) | Welcome Message sent, logged")
        except Exception as e:
            logger.error(f"Error in running on_member_join event {member}: {e}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            guild = member.guild
            log_channel = guild.get_channel(log_channel_id)
            log_embed=discord.Embed(title="Member Left", description=f"<@{member.id}> **({member.id})** has left the server.", color=bot_color)
            log_embed.set_author(name=f"{member}", icon_url=f"{member.avatar_url}")   
            log_embed.set_footer(text=f"Member Count: {guild.member_count}")
            log_embed.timestamp = datetime.datetime.utcnow()
            await log_channel.send(embed=log_embed)
            
            logger.info(f"A member has left: {member} ({member.id}) | Message has been logged")
        except Exception as e:
            logger.error(f"Error in logging on_member_remove {member.name}: {e}")
    
    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        try:
            msg_obj = payload.cached_message
            if msg_obj:
                msg = msg_obj.content
                # print(msg)

                log_channel = discord.utils.get(self.client.get_all_channels(),id=log_channel_id)
                log_embed = discord.Embed(title="Message Deleted", color=bot_color)
                log_embed.set_author(name=f"{msg_obj.author}", icon_url=f"{msg_obj.author.avatar_url}")
                log_embed.add_field(name="Sent Message", value=f"{msg}", inline=False)
                log_embed.add_field(name="Channel", value=f"{msg_obj.channel}", inline=False)
                log_embed.timestamp = datetime.datetime.utcnow()
                log_embed.set_footer(text="Micro Logs")
                await log_channel.send(embed=log_embed)
                
                logger.info(f"Deleted message by {msg_obj.author} ({msg_obj.author.id}) has been logged | {msg_obj.content.encode('utf-8')}")
        
        except Exception as e:
            # print('erorr',e)
            logger.error(f"Error in logging on_message_remove: {e}")

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        msg = payload.message_id
        c_id = payload.channel_id
        channel = discord.utils.get(self.client.get_all_channels(),id=c_id)
        
        msg_obj = await channel.fetch_message(msg)
        new_msg = msg_obj.content.strip()
        old_msg = payload.cached_message.content.strip() if payload.cached_message is not None else ''

        guild = msg_obj.channel.guild
        log_channel = guild.get_channel(log_channel_id)

        fmt_msg = new_msg.strip().lower().split(' ')
        # print(new_msg)
        if old_msg == new_msg: # Fixes the link embed triggering 
            return
        
        strict = insult.isItInsult(fmt_msg)[0]
        lenient = insult.isItInsult(fmt_msg)[1] 
        if lenient:
            try:
                await msg_obj.delete()
                
                profanity_embed=discord.Embed(description=f"Please avoid the use of profanity. <@{msg_obj.author.id}>", color=bot_color)
                await msg_obj.channel.send(embed=profanity_embed)
                
                log_embed = discord.Embed(title="Profanity Filter (Modified Message)", color=bot_color)
                log_embed.set_author(name=f"{msg_obj.author}", icon_url=f"{msg_obj.author.avatar_url}")
                log_embed.add_field(name="Original Message", value=f"{old_msg if old_msg else 'N/A'}", inline=False)
                log_embed.add_field(name="Modified Message", value=f"{new_msg}", inline=False)
                log_embed.add_field(name="Channel", value=f"{channel.name}", inline=False)
                log_embed.timestamp = datetime.datetime.utcnow()
                log_embed.set_footer(text="Micro Logs")
                await log_channel.send(embed=log_embed)
            
                logger.info(f"The modified message from [{old_msg if old_msg else 'N/A'}] to [{new_msg}] was Deleted | User: {msg_obj.author}")
            
                return
            
            except Exception as e:
                # print('error')
                logger.error(f"Couldn't delete the message {e}")  
        
        elif strict:
            try: 
                logger.info(f"The Message [{msg_obj.content}] is potentially profane | User: {msg_obj.author.name}")

                guild = msg_obj.channel.guild
                mod_channel = guild.get_channel(mod_channel_id)
                log_embed = discord.Embed(title="Potential Profane Word found", color=bot_color)
                log_embed.set_author(name=f"{msg_obj.author}", icon_url=f"{msg_obj.author.avatar_url}")
                log_embed.add_field(name="Sent Message", value=f"{msg_obj.content}", inline=False)
                log_embed.add_field(name="Channel", value=f"{msg_obj.channel}", inline=False)
                log_embed.add_field(name="URL", value=f"[Link to the message]({msg_obj.jump_url})", inline=False)
                log_embed.timestamp = datetime.datetime.utcnow()
                log_embed.set_footer(text="Micro Logs")
                embed = await mod_channel.send(embed=log_embed)

                await embed.add_reaction("✅")
                await embed.add_reaction("❌")

                return 
            
            except Exception as e:
                print(e)
                logger.error(f"Couldn't detect the profane message {e}")
   
        else:
            log_embed = discord.Embed(title="Modified Message", color=bot_color)
            log_embed.set_author(name=f"{msg_obj.author}", icon_url=f"{msg_obj.author.avatar_url}")
            log_embed.add_field(name="Original Message", value=f"{old_msg if old_msg else 'N/A'}", inline=False)
            log_embed.add_field(name="Modified Message", value=f"{new_msg}", inline=False)
            log_embed.add_field(name="Channel", value=f"{channel.name}", inline=False)
            log_embed.timestamp = datetime.datetime.utcnow()
            log_embed.set_footer(text="Micro Logs")
            await log_channel.send(embed=log_embed)
            
            logger.info(f"The modified message from [{old_msg.encode('utf-8') if old_msg else 'N/A'}] to [{new_msg.encode('utf-8')}] was logged | User: {msg_obj.author}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload): 
        mod_channel = discord.utils.get(self.client.get_all_channels(),id=payload.channel_id)
        member = payload.member
        msg_obj = await mod_channel.fetch_message(payload.message_id)
        reactions = msg_obj.reactions
        manage_msg_perm = member.permissions_in(mod_channel).manage_messages
        # moderator = discord.utils.get(mod_channel.guild.roles,name='Moderator')
        users_that_are_bot = []
        
        if not manage_msg_perm:
            return

        if member.bot:
            return
        else:
            for reaction in msg_obj.reactions:
                async for user in reaction.users():
                    users_that_are_bot.append(user.bot)

        for reaction in reactions:
            if reaction.emoji == '❌' and reaction.count >= 2 and any(users_that_are_bot):
                embed = msg_obj.embeds[0]
                link = embed.fields[-1].value.split('(')[-1][:-1]
                cid, mid = int(link.split('/')[-2]), int(link.split('/')[-1])

                channel = discord.utils.get(self.client.get_all_channels(), id=cid)
                try:
                    msg = await channel.fetch_message(mid)
                except discord.NotFound:
                    temp_embed = discord.Embed(description=f"The potentially profane message has already been deleted.", color=bot_color)
                    
                    await reaction.message.delete()
                    await mod_channel.send(embed=temp_embed,delete_after=5)
                    return

                await msg.delete()
                await reaction.message.delete()

                temp_embed = discord.Embed(description=f"The potentially profane message has been deleted.", color=bot_color)
                await mod_channel.send(embed=temp_embed,delete_after=5)
                
                return

            elif reaction.emoji == '✅' and reaction.count >= 2 and any(users_that_are_bot):
                await reaction.message.delete()

                temp_embed = discord.Embed(description=f"The message has been marked as non profane.", color=bot_color)
                await mod_channel.send(embed=temp_embed,delete_after=5)
                
                return            

    @commands.Cog.listener()
    async def on_message(self, message):
        #ignore it if it's from the bot
        if message.author == self.client:
            return
        
        #prepare the message into list of words 
        msg = message.content.lower().strip().replace('\n',' ').split(' ')
        strict = insult.isItInsult(msg)[0]
        lenient = insult.isItInsult(msg)[1]

        if not msg: # If list is empty - []
            return
        
        elif lenient:
            try:
                await message.delete()
                
                logger.info(f"The Message [{message.content.encode('utf-8')}] was Deleted | User: {message.author.name}")
                profanity_embed = discord.Embed(description=f"Please avoid the use of profanity. <@{message.author.id}>", color=0x00afb1)
                await message.channel.send(embed=profanity_embed)
                
                guild = message.channel.guild
                log_channel = guild.get_channel(log_channel_id)
                log_embed = discord.Embed(title="Profanity Filter", color=bot_color)
                log_embed.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar_url}")
                log_embed.add_field(name="Sent Message", value=f"{message.content}", inline=False)
                log_embed.add_field(name="Channel", value=f"{message.channel}", inline=False)
                log_embed.timestamp = datetime.datetime.utcnow()
                log_embed.set_footer(text="Micro Logs")
                await log_channel.send(embed=log_embed)
                return 
            
            except Exception as e:
                logger.error(f"Couldn't delete the message {e}")

        elif strict:
            try: 
                logger.info(f"The Message [{message.content.encode('utf-8')}] is potentially profane | User: {message.author.name}")

                guild = message.channel.guild
                mod_channel = guild.get_channel(mod_channel_id)
                log_embed = discord.Embed(title="Potential Profane Word found", color=bot_color)
                log_embed.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar_url}")
                log_embed.add_field(name="Sent Message", value=f"{message.content}", inline=False)
                log_embed.add_field(name="Channel", value=f"{message.channel}", inline=False)
                log_embed.add_field(name="URL", value=f"[Jump to the message]({message.jump_url})", inline=False)
                log_embed.timestamp = datetime.datetime.utcnow()
                log_embed.set_footer(text="Micro Logs")
                embed = await mod_channel.send(embed=log_embed)

                await embed.add_reaction("✅")
                await embed.add_reaction("❌")

                return 
            
            except Exception as e:
                print(e)
                logger.error(f"Couldn't detect the profane message {e}")

        elif message.content == 'F':
            await message.channel.send('Respekt :3')

def setup(client):
    client.add_cog(Events(client))