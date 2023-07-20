import discord
from discord.ext import commands
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class Statistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Statistics commands here

    async def get_server_activity(self, guild):
        activity_data = []

        # Get server activity for the last 7 days
        for i in range(7, 0, -1):
            activity = {
                'day': i,
                'messages': 0,
                'members_joined': 0,
                'members_left': 0
            }

            # Get activity for each day
            async for entry in guild.audit_logs(limit=None, oldest_first=False):
                if entry.created_at.date() == (datetime.utcnow().date() - timedelta(days=i)):
                    if entry.action.name == 'member_join':
                        activity['members_joined'] += 1
                    elif entry.action.name == 'member_remove':
                        activity['members_left'] += 1

            activity_data.append(activity)

        return activity_data

    @commands.command()
    async def server(self, ctx):
        guild = ctx.guild

        # Total Members
        total_members = guild.member_count

        # Text Channels
        text_channels = len(guild.text_channels)

        # Voice Channels
        voice_channels = len(guild.voice_channels)

        # Categories
        categories = len(guild.categories)

        # Create and send the server stats embed
        embed = discord.Embed(title=f"{guild.name} Server Stats", color=discord.Color.green())
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="Total Members", value=total_members, inline=False)
        embed.add_field(name="Text Channels", value=text_channels, inline=False)
        embed.add_field(name="Voice Channels", value=voice_channels, inline=False)
        embed.add_field(name="Categories", value=categories, inline=False)

        # Get server activity data
        activity_data = await self.get_server_activity(guild)

        # Generate a line graph for server activity
        days = np.arange(1, len(activity_data) + 1)
        messages = [data['messages'] for data in activity_data]
        members_joined = [data['members_joined'] for data in activity_data]
        members_left = [data['members_left'] for data in activity_data]

        # Create the line graph
        plt.figure(figsize=(10, 6))
        plt.plot(days, messages, label='Messages')
        plt.plot(days, members_joined, label='Members Joined')
        plt.plot(days, members_left, label='Members Left')

        plt.xlabel('Days')
        plt.ylabel('Count')
        plt.title('Server Activity')
        plt.legend()

        # Save the line graph as an image
        plt.savefig('line_graph.png')
        plt.close()

        # Add the line graph image to the embed
        file = discord.File('line_graph.png', filename='line_graph.png')
        embed.set_image(url='attachment://line_graph.png')

        # Send the server stats embed with the line graph image
        await ctx.send(embed=embed, file=file)

def setup(bot):
    bot.add_cog(Statistics(bot))
