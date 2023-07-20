import discord
from discord.ext import commands
import asyncio
from cogs.general import General
from cogs.calendar import Calendar
from cogs.social import Social
from cogs.statistics import Statistics

# Set up the bot prefix
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Load cogs
extensions = ['cogs.general', 'cogs.statistics', 'cogs.calendar', 'cogs.social']

async def load_extensions():
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"Loaded extension: {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}: {str(e)}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

# Using regular await syntax to load the extensions in an asynchronous manner
async def run_bot():
    await bot.wait_until_ready()
    await load_extensions()

# Running the bot with the correct token
bot.run('ID')
