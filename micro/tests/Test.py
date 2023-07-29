import discord
from discord.ext import commands

class Test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='test')
    async def command(self, ctx):
        await ctx.send("hi")

    
def setup(client):
    client.add_cog(Test(client))