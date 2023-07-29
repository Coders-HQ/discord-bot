import discord
from discord.ext import commands
from logger import logger as loggger
import static.constants as constants

log_channel = constants.LOG_CHANNELID

#initalizing logger
logger = loggger()

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='kick')
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        try:   
            await ctx.message.delete()
            await member.kick(reason=reason)
            kickembed=discord.Embed(description=f"<@{member.id}> has been kicked by <@{ctx.author.id}>.", color=0x00afb1)
            await ctx.send(embed=kickembed)
            kicklog=discord.Embed(color=0x00afb1)
            kicklog.add_field(name="Moderator", value=f"<@{ctx.author.id}>", inline=True)
            kicklog.add_field(name="Offender", value=f"<@{member.id}>", inline=True)
            kicklog.add_field(name="Action", value="Kick", inline=True)
            kicklog.add_field(name="Reason", value=f"{reason}", inline=False)
            await ctx.guild.get_channel(log_channel).send(embed=kicklog)
            logger.info(f"{member.name} ({member.id}) was kicked by {ctx.author.name} | Reason: {reason}")
        except Exception as e:
            kickerror=discord.Embed(description=f"Could not kick <@{member.id}>.", color=0x00afb1)
            await ctx.send(embed=kickerror)
            logger.error(f"Could not kick {member.name} ({member.id}) {e}")

    @commands.command(name='ban')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        try:
            await ctx.message.delete()
            await member.ban(reason=reason)
            banembed=discord.Embed(description=f"<@{member.id}> has been banned by <@{ctx.author.id}>.", color=0x00afb1)
            await ctx.send(embed=banembed)
            banlog=discord.Embed(color=0x00afb1)
            banlog.add_field(name="Moderator", value=f"<@{ctx.author.id}>", inline=True)
            banlog.add_field(name="Offender", value=f"<@{member.id}>", inline=True)
            banlog.add_field(name="Action", value="Ban", inline=True)
            banlog.add_field(name="Reason", value=f"{reason}", inline=False)
            await ctx.guild.get_channel(log_channel).send(embed=banlog)
            logger.info(f"{member.name} ({member.id}) was banned by {ctx.author.name} | Reason: {reason}")
        except Exception as e:
            banerror=discord.Embed(description=f"Could not ban <@{member.id}>.", color=0x00afb1)
            await ctx.send(embed=banerror)
            logger.error(f"Could not ban {member.name} ({member.id}) {e}")

    @commands.command(name='unban')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *,member):
        try:
            ban_list = await ctx.guild.bans()
            user_name, user_discriminator = member.split('#')

            for banned_user in ban_list:
                user = banned_user.user
                if (user.name, user.discriminator) == (user_name, user_discriminator):
                    await ctx.message.delete()
                    await ctx.guild.unban(user)
                    unbanembed=discord.Embed(description=f"<@{user.id}> has been unbanned.", color=0x00afb1)
                    await ctx.send(embed=unbanembed)
                    unbanlog=discord.Embed(color=0x00afb1)
                    unbanlog.add_field(name="Moderator", value=f"<@{ctx.author.id}>", inline=True)
                    unbanlog.add_field(name="Offender", value=f"<@{user.id}>", inline=True)
                    unbanlog.add_field(name="Action", value="Unban", inline=True)
                    await ctx.guild.get_channel(log_channel).send(embed=unbanlog)
                    logger.info(f"{user} ({user.id}) was unbanned by {ctx.author}")
        except Exception as e:
            unbanerror=discord.Embed(description=f"Could not unban <@{user.id}>.", color=0x00afb1)
            await ctx.send(embed=unbanerror)
            logger.error(f"Could not unban {user} ({user.id}) {e}")

    @commands.command(name='mute')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason: str = None):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            wrong_config = discord.Embed(description=f"Role not configured correctly.", color=0x00afb1)
            return await ctx.send(embed=wrong_config)
        try:
            await member.add_roles(muted_role, reason=reason) #pottential erro MemberNotFound
            
            muted_embed = discord.Embed(description=f"<@{member.id}> has been muted.", color=0x00afb1)
            await ctx.send(embed=muted_embed)
            
            mute_log = discord.Embed(color=0x00afb1)
            mute_log.add_field(name="Moderator", value=f"<@{ctx.author.id}>", inline=True)
            mute_log.add_field(name="Offender", value=f"<@{member.id}>", inline=True)
            mute_log.add_field(name="Action", value="Mute", inline=True)
            mute_log.add_field(name="Reason", value=f"{reason}", inline=False)
            await ctx.guild.get_channel(log_channel).send(embed=mute_log)
            
            logger.info(f"{member.name} ({member.id}) was muted by {ctx.author.name} | Reason: {reason}")
        
        except Exception as e:
            mute_error = discord.Embed(description=f"Could not mute <@{member.id}>.", color=0x00afb1)
            await ctx.send(embed=mute_error)
            
            logger.error(f"Could not mute {member.name} ({member.id}) {e}")

    @commands.command(name='unmute')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = None):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            wrong_config = discord.Embed(description=f"Role not configured correctly.", color=0x00afb1)
            return await ctx.send(embed=wrong_config)
        try:
            await member.remove_roles(muted_role, reason=reason)
            unmuted_embed = discord.Embed(description=f"<@{member.id}> has been unmuted.", color=0x00afb1)
            await ctx.send(embed=unmuted_embed)
            
            unmute_log = discord.Embed(color=0x00afb1)
            unmute_log.add_field(name="Moderator", value=f"<@{ctx.author.id}>", inline=True)
            unmute_log.add_field(name="Offender", value=f"<@{member.id}>", inline=True)
            unmute_log.add_field(name="Action", value="Unmute", inline=True)
            unmute_log.add_field(name="Reason", value=f"{reason}", inline=False)
            await ctx.guild.get_channel(log_channel).send(embed=unmute_log)
            
            logger.info(f"{member.name} ({member.id}) was unmuted by {ctx.author.name}")
        
        except Exception as e:
            mute_error = discord.Embed(description=f"Could not unmute <@{member.id}>.", color=0x00afb1)
            await ctx.send(embed=mute_error)
            logger.error(f"Could not unmute {member.name} ({member.id}) {e}")
            print(e)
    
    @commands.command(name='purge')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=0, member: discord.Member=None):
        try:
            msgs = []
            purge_log = discord.Embed(color=0x00afb1)
            if member is None:
                await ctx.channel.purge(limit=amount + 1)
                
                purge_embed = discord.Embed(description=f"{amount} messages have been purged.", color=0x00afb1)
                await ctx.send(embed=purge_embed)
                
                logger.info(f"{amount} messages have been purged.")
                purge_log.add_field(name="Moderator", value=f"<@{ctx.author.id}>", inline=False)
                purge_log.add_field(name="Action", value="Purge", inline=False)
                purge_log.add_field(name="Result", value=f"Purged {amount} messages", inline=False)
                await ctx.guild.get_channel(log_channel).send(embed=purge_log)
            
            else:
                # print([x.content for x in await ctx.channel.history(limit=amount).flatten()])
                for m in await ctx.channel.history().flatten():
                    if len(msgs) == amount:
                        break
                    if m.author == member:
                        msgs.append(m)
                
                await ctx.channel.delete_messages(msgs)
                
                text = f"{amount} {'messages' if amount > 1 else 'message'} have been purged of <@{member.id}>."
                purge_embed = discord.Embed(description=text, color=0x00afb1)
                await ctx.send(embed=purge_embed)

        except Exception as e:
            purge_error = discord.Embed(description=f"Could not purge messsages.", color=0x00afb1)
            await ctx.send(embed=purge_error)
            
            logger.error(f"Could not purge messages. {e}")
        

def setup(client):
    client.add_cog(Moderation(client))