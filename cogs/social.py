import discord
from discord.ext import commands

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reaction_roles = {}

    # Command: Add reaction role
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def add_reaction_role(self, ctx, role: discord.Role, message_id: int, emoji):
        message = await ctx.channel.fetch_message(message_id)
        await message.add_reaction(emoji)
        self.reaction_roles[message_id] = {'emoji': emoji, 'role_id': role.id}

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id in self.reaction_roles:
            guild_id = payload.guild_id
            guild = self.bot.get_guild(guild_id)
            role_id = self.reaction_roles[payload.message_id]['role_id']
            role = discord.utils.get(guild.roles, id=role_id)
            if role is not None:
                member = guild.get_member(payload.user_id)
                if member is not None:
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id in self.reaction_roles:
            guild_id = payload.guild_id
            guild = self.bot.get_guild(guild_id)
            role_id = self.reaction_roles[payload.message_id]['role_id']
            role = discord.utils.get(guild.roles, id=role_id)
            if role is not None:
                member = guild.get_member(payload.user_id)
                if member is not None:
                    await member.remove_roles(role)

    @commands.command()
    async def create_poll(self, ctx, question, *options):
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

    @commands.Cog.listener()
    async def on_raw_reaction_addpoll(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)

        if reaction and not message.author.bot:
            if reaction.count >= 3:  # Adjust the minimum required reactions here
                embed = discord.Embed(description=f"The poll '{message.content}' has received enough votes.", color=discord.Color.green())
                await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Social(bot))
