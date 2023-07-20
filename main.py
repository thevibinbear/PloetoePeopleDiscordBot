import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Load cogs
extensions = ['cogs.general', 'cogs.statistics', 'cogs.calendar', 'cogs.social']

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)

# Other settings here

# Run the bot
bot.run('ID')
