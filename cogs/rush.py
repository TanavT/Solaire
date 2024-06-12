import discord
from discord.ext import commands
from ui.views.rushH.GameSettings import GameSettings
from ui.views.rushH.PlayerJoin import PlayerJoin
import cogs.helper.rushH as Helper


views = None
players = None
MAX_SLOTS = 4
game_choices = ["Elden Ring", "Hollow Knight", "Super Mario 64"]


class RushMain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def rush(self, ctx):
        global players
        global MAX_SLOTS
        global views
        global game_choices

        # variables
        players = MAX_SLOTS * [""]

        views = [PlayerJoin("| Waiting for Players...", players), GameSettings("| Game Settings..."), None,
                 ]

        await ctx.respond("| Starting Rush Mini-Game!")

        # running rush
        for view in views:
            await ctx.send(view.message, view=view)
            await view.wait()

            if view.exit_triggered:
                break

            if view == views[1]:
                if views[1].game_choice not in game_choices:
                    await ctx.send("Could not find chosen game")
                    raise ValueError("Error: Game Chosen is not Implemented")
                views[2] = Helper.lookup_game_view(views[1].game_choice, game_choices)

        await ctx.send(f"The choice picked was {views[1].game_choice} and {views[1].mode_choice} and score is {views[1].score_choice}")


def setup(bot):
    bot.add_cog(RushMain(bot))
