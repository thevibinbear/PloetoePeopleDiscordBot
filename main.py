import discord
from discord.ext import commands
import datetime
import asyncio

# Set up the bot prefix
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
CHANNEL_ID = ""
reminders = {}
# Dictionary to store message ID and corresponding roles
reaction_roles = {}

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

# Event: When a new member joins the server
@bot.event
async def on_member_join(member):
    # Customize the welcome message
    welcome_message = f"Welcome, {member.mention}! Enjoy your stay."

    # Send the welcome message to a specific channel (replace CHANNEL_ID with the channel ID)
    channel = bot.get_channel(CHANNEL_ID)

    embed = discord.Embed(description=welcome_message, color=discord.Color.green())
    await channel.send(embed=embed)

# Event: When a member leaves the server
@bot.event
async def on_member_remove(member):
    # Customize the farewell message
    farewell_message = f"Goodbye, {member.display_name}. We'll miss you!"

    # Send the farewell message to a specific channel (replace CHANNEL_ID with the channel ID)
    channel = bot.get_channel(CHANNEL_ID)

    embed = discord.Embed(description=farewell_message, color=discord.Color.red())
    await channel.send(embed=embed)

# Command: Ping
@bot.command()
async def ping(ctx):
    embed = discord.Embed(description='Pong!', color=discord.Color.blue())
    await ctx.send(embed=embed)

# Command: Say
@bot.command()
async def say(ctx, *, message):
    embed = discord.Embed(description=message, color=discord.Color.green())
    await ctx.send(embed=embed)

# Command: Kick
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed = discord.Embed(description=f'{member.display_name} has been kicked.', color=discord.Color.red())
    await ctx.send(embed=embed)

# Command: Ban
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed = discord.Embed(description=f'{member.display_name} has been banned.', color=discord.Color.red())
    await ctx.send(embed=embed)

# Command: Purge
@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(description=f'{amount} messages have been purged.', color=discord.Color.blue())
    await ctx.send(embed=embed)

# Command: Add reaction role
@bot.command()
@commands.has_permissions(manage_roles=True)
async def add_reaction_role(ctx, role: discord.Role, message_id: int, emoji):
    message = await ctx.channel.fetch_message(message_id)
    await message.add_reaction(emoji)
    reaction_roles[message_id] = {'emoji': emoji, 'role_id': role.id}

# Event: Reaction added
@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id in reaction_roles:
        guild_id = payload.guild_id
        guild = bot.get_guild(guild_id)
        role_id = reaction_roles[payload.message_id]['role_id']
        role = discord.utils.get(guild.roles, id=role_id)
        if role is not None:
            member = guild.get_member(payload.user_id)
            if member is not None:
                await member.add_roles(role)

# Event: Reaction removed
@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id in reaction_roles:
        guild_id = payload.guild_id
        guild = bot.get_guild(guild_id)
        role_id = reaction_roles[payload.message_id]['role_id']
        role = discord.utils.get(guild.roles, id=role_id)
        if role is not None:
            member = guild.get_member(payload.user_id)
            if member is not None:
                await member.remove_roles(role)

@bot.command()
async def server_stats(ctx):
    # Get server information
    guild = ctx.guild
    total_members = guild.member_count
    total_channels = len(guild.channels)
    total_text_channels = len(guild.text_channels)
    total_voice_channels = len(guild.voice_channels)
    total_categories = len(guild.categories)

    # Get message count
    message_count = 0
    for channel in guild.text_channels:
        async for _ in channel.history(limit=None):
            message_count += 1

    # Create server stats embed
    embed = discord.Embed(title="Server Statistics", color=discord.Color.blue())
    embed.add_field(name="Total Members", value=total_members)
    embed.add_field(name="Total Channels", value=total_channels)
    embed.add_field(name="Total Text Channels", value=total_text_channels)
    embed.add_field(name="Total Voice Channels", value=total_voice_channels)
    embed.add_field(name="Total Categories", value=total_categories)
    embed.add_field(name="Total Messages", value=message_count)

    await ctx.send(embed=embed)

# Command: Set reminder
@bot.command()
async def remind(ctx, duration: int, *, reminder: str):
    current_time = datetime.datetime.now()
    future_time = current_time + datetime.timedelta(minutes=duration)

    # Store reminder in the dictionary
    reminders[reminder] = future_time

    embed = discord.Embed(description=f"Reminder set for {duration} minutes from now.", color=discord.Color.blue())
    await ctx.send(embed=embed)

    # Wait for the reminder duration
    await asyncio.sleep(duration * 60)

    # Check if the reminder is still valid
    if reminder in reminders and reminders[reminder] == future_time:
        embed = discord.Embed(description=f"Reminder: {reminder}", color=discord.Color.green())
        await ctx.send(embed=embed)

        # Remove the reminder from the dictionary
        del reminders[reminder]

# Command: Set timer
@bot.command()
async def timer(ctx, duration: int):
    embed = discord.Embed(description=f"Timer set for {duration} seconds.", color=discord.Color.blue())
    await ctx.send(embed=embed)

    # Wait for the timer duration
    await asyncio.sleep(duration)

    embed = discord.Embed(description=f"Timer ended for {duration} seconds.", color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command()
async def create_poll(ctx, question, *options):
    if len(options) <= 1:
        embed = discord.Embed(description="Please provide at least 2 options for the poll.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    formatted_options = [f"{i + 1}. {option}" for i, option in enumerate(options)]
    poll_message = f"{question}\n\n" + "\n".join(formatted_options)

    embed = discord.Embed(title="Poll", description=poll_message, color=discord.Color.blue())

    poll = await ctx.send(embed=embed)

    for i in range(len(options)):
        emoji = chr(0x1f1e6 + i)
        option = options[i]
        embed.add_field(name=emoji, value=option, inline=False)
        await poll.add_reaction(emoji)

    await poll.edit(embed=embed)

@bot.event
async def on_raw_reaction_addpoll(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)

    if reaction and not message.author.bot:
        if reaction.count >= 3:  # Adjust the minimum required reactions here
            embed = discord.Embed(description=f"The poll '{message.content}' has received enough votes.", color=discord.Color.green())
            await channel.send(embed=embed)

# Run the bot
bot.run('ID')
