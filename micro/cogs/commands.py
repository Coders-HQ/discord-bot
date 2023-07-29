import discord
from discord.ext import commands
from logger import logger as loggger
from classes.QuestionQuery import QuestionQuery
from classes.resources import Resources
from datetime import timezone, datetime
import static.constants as constants

#initalizing logger
logger = loggger()

Questions = QuestionQuery('static/questions.xlsx',logger)
resources = Resources()

COLOR = constants.BOT_COLOR

class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='chq')
    async def chq(self, ctx, arg=None):
        try:  
            if arg==None:
                answer = Questions.question("who")
                logger.info(f"a reply was sent to {ctx.author.name}")
                await ctx.send(embed=answer)    
            else:
                arg2 = arg.lower()
                answer = Questions.question(arg2)
                logger.info(f"a reply was sent to {ctx.author.name}")
                await ctx.send(embed=answer)
        except Exception as e:
            chqerror=discord.Embed(description=f"Error sending response.", color=0x00afb1)
            await ctx.send(embed=chqerror)
            logger.error(f"Error sending a reply on the !chq command to user {ctx.author.name} | {e}")     

    @commands.command(name='count')
    async def count(self, ctx):
        try:  
            member_count = len([member for member in await ctx.guild.fetch_members().flatten() if not member.bot])
            count_embed = discord.Embed(description=f"Member Count: {member_count}", color=0x00afb1)
            
            await ctx.send(embed=count_embed)
        
        except Exception as e:
            chqerror = discord.Embed(description=f"Error in sending response.", color=0x00afb1)
            await ctx.send(embed=chqerror)
            logger.error(f"Error sending a reply | {e}")   

    @commands.command(name='resources')
    async def resources(self, ctx, topic: str=''):
        try:
            resources.reload_resource('static/resources.json')
            if not topic:
                embed = discord.Embed(description="Learning resources selected by the community, for the community",color=0x00afb1)
                for lang,lang_resc in resources.get_kw_lang_map().items():
                    if len(lang_resc) >= 2:
                        embed.add_field(name=f'{lang} resources',value=f'Use `!resources {lang_resc[0]}` or `!resources {lang_resc[1]}`',inline=False)    
                    else:
                        embed.add_field(name=f'{lang} resources',value=f'Use `!resources {lang_resc[0]}`',inline=False)    
                await ctx.channel.send(embed=embed)
                logger.info(f'Resources list was sent as requested by <@{ctx.author}>')   
            
            else:
                for lang,kw in resources.get_all_kw().items():
                    if topic in kw:
                        data = resources.get_details(lang)
                        embed = discord.Embed(title=lang, color=0x00afb1)
                        for category,contents in data.items():
                            text = ''
                            if category == 'Keywords':
                                break
                            if category == 'Description':
                                text = contents
                                embed.add_field(name=category,value=text,inline=False)
                           
                            else:
                                for content in contents:
                                    title = content.split(' - ')
                                    if len(title) > 1:
                                        link = title[-1]
                                        name = ' - '.join(title[:-1])
                                        text += f"[{name}]({link})\n"
                                    else:
                                        link = content
                                        text += f"{link}\n"
                                embed.add_field(name=category,value=text,inline=False)
                        
                        await ctx.channel.send(embed=embed)
                        
                        logger.info(f'Resource for {lang} was sent as requested by <@{ctx.author}>')
                        
                        break
        
        except Exception as e:
            logger.info(f'Error in running !resources command: {e}')

    @commands.command(name='serverage')
    async def serverage(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        else:
            member = member

        dt_joined = member.joined_at.replace(tzinfo=timezone.utc)
        dt_now = datetime.now(tz=timezone.utc)
        delta = dt_now - dt_joined
        days = delta.days
        hours = delta.seconds // 3600
        embed = discord.Embed(description=f'<@{member.id}> have been under the watch of Micro for {days} days and {hours} hours🎉')
        await ctx.channel.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.channel.send("Pong!")

    @commands.command(name='help')
    async def help(self,ctx):
        try:
            author = ctx.author
            admin_role = discord.utils.get(ctx.guild.roles,name='Admin')
            mod_role = discord.utils.get(ctx.guild.roles,name='Moderator')
            
            
            if admin_role in author.roles or mod_role in author.roles:
                cmds = constants.ALL_COMMANDS
            else:
                cmds = constants.USER_COMMANDS
            
            embed = discord.Embed(title="List of bot commands",color=COLOR)
            for cmd,desc in cmds.items():
                embed.add_field(name=cmd,value=desc,inline=False)
            
            await ctx.send(embed=embed)
            logger.info(f'Successfully sent help commands on request by {author}({author.id})')
        
        except Exception as e:
            logger.info(f'Failed to run help command: {e}')
    
def setup(client):
    client.add_cog(Commands(client))