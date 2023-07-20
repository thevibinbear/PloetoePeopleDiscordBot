import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command: Ping
    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(description='Pong!', color=discord.Color.blue())
        await ctx.send(embed=embed)

    # Command: Say
    @commands.command()
    async def say(self, ctx, *, message):
        embed = discord.Embed(description=message, color=discord.Color.green())
        await ctx.send(embed=embed)

    # Command: Kick
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        embed = discord.Embed(description=f'{member.display_name} has been kicked.', color=discord.Color.red())
        await ctx.send(embed=embed)

    # Command: Ban
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embed = discord.Embed(description=f'{member.display_name} has been banned.', color=discord.Color.red())
        await ctx.send(embed=embed)

    # Command: Purge
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(description=f'{amount} messages have been purged.', color=discord.Color.blue())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))
