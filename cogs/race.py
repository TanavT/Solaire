import discord
from discord.ext import commands
from ui.views.PlayerJoin import PlayerJoin
from ui.views.raceH.GameSettings import GameSettings
import cogs.helper.raceH.lookup_game as lookup

views = None
players = None
MAX_SLOTS = 20
game_choices = ["Elden Ring", "Hollow Knight", "Super Mario Odyssey"]

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
                 None, None]

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
            elif iterator == 1:
                if views[iterator].game_choice not in game_choices:
                    await ctx.send("Could not find chosen game")
                    raise ValueError("Error: Game Chosen is not Implemented")
                views[iterator+1] = lookup.lookup_game_view(views[1].game_choice, game_choices, players,
                                                            views[iterator].difficulty)
            iterator += 1


def setup(bot):
    bot.add_cog(Race(bot))
