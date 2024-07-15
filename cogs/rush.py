import discord
from discord.ext import commands
from ui.views.rushH.GameSettings import GameSettings
from ui.views.rushH.PlayerJoin import PlayerJoin
from ui.views.rushH.RunningGame import RunningGame
import cogs.helper.rushH.lookup_game as lookup


views = None
players = None
MAX_SLOTS = 4
game_choices = ["Elden Ring", "Hollow Knight", "Super Mario Odyssey"]


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

        views = [PlayerJoin("| Waiting for Players...", players),
                 GameSettings("| Game Settings... (Only Elden Ring is currently implemented)", players),
                 None, None]

        await ctx.respond("| Starting Rush Mini-Game!")

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
                views[iterator+1] = lookup.lookup_game_view(views[1].game_choice, game_choices, players)
            elif iterator == 2:
                running_game_view = RunningGame("| Game Started! Click 'Start!' to start the game and click "
                                                "'Finished!' when you completed a goal",
                                                players, views[iterator].goal_list,
                                                views[iterator].pattern_choice, views[iterator].color,
                                                views[iterator-1].score_choice, views[iterator-1].mode_choice,
                                                views[iterator].goal_choices, views[iterator-1].setup_choice)
                views[iterator+1] = running_game_view
            iterator += 1

        # await ctx.send(f"The choice picked was {views[1].game_choice} and {views[1].mode_choice} and score is
        # {views[1].score_choice}")


def setup(bot):
    bot.add_cog(RushMain(bot))
