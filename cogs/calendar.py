import discord
from discord.ext import commands
import datetime
import asyncio

class Calendar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = {}

    # Command: Set reminder
    @commands.command()
    async def remind(self, ctx, duration: int, *, reminder: str):
        current_time = datetime.datetime.now()
        future_time = current_time + datetime.timedelta(minutes=duration)

        # Store reminder in the dictionary
        self.reminders[reminder] = future_time

        embed = discord.Embed(description=f"Reminder set for {duration} minutes from now.", color=discord.Color.blue())
        await ctx.send(embed=embed)

        # Wait for the reminder duration
        await asyncio.sleep(duration * 60)

        # Check if the reminder is still valid
        if reminder in self.reminders and self.reminders[reminder] == future_time:
            embed = discord.Embed(description=f"Reminder: {reminder}", color=discord.Color.green())
            await ctx.send(embed=embed)

            # Remove the reminder from the dictionary
            del self.reminders[reminder]

    # Command: Set timer
    @commands.command()
    async def timer(self, ctx, duration: int):
        embed = discord.Embed(description=f"Timer set for {duration} seconds.", color=discord.Color.blue())
        await ctx.send(embed=embed)

        # Wait for the timer duration
        await asyncio.sleep(duration)

        embed = discord.Embed(description=f"Timer ended for {duration} seconds.", color=discord.Color.green())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Calendar(bot))
