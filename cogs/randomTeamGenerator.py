import discord
from discord.ext import commands


class RandomTeamMain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def generate_random_team(self, ctx):
        await ctx.respond(embed = discord.Embed())

def setup(bot):
    bot.add_cog(RandomTeamMain(bot))
