import discord
from discord.ext import commands
from ui.views.PlayerJoin import PlayerJoin
from ui.views.raceH.GameSettings import GameSettings

views = None
players = None
MAX_SLOTS = 20


class Race(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def race(self, ctx):
        global players
        global MAX_SLOTS
        global views

        # variables
        players = MAX_SLOTS * [""]

        views = [PlayerJoin("| Waiting for Players...", players),
                 GameSettings("| Game Settings... (Only Elden Ring is currently implemented)", players),
                 None]

        await ctx.respond("| Starting Race Mini-Game!")

        # running rush
        iterator = 0
        for view in views:
            await ctx.send(content=view.message_str, view=view)
            await view.wait()

            if view.exit_triggered:
                break
            if iterator == 0:
                while "" in players:
                    players.remove("")
            iterator += 1


def setup(bot):
    bot.add_cog(Race(bot))
