import re
import discord
from discord.ext import commands
from ui.views.PlayerJoin import PlayerJoin
from ui.views.randomTeamGeneratorH.TeamSettings import TeamSettings
from ui.views.randomTeamGeneratorH.TeamGeneration import TeamGeneration



class PlayersModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="Players", placeholder="Player 1, Player 2, Player3, ...",
                                           style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Number of Teams", value="2"))

    async def callback(self, interaction: discord.Interaction):
        player_list_re = re.compile("^\s*[^,\s][^,]*(?:\s*,\s*[^,\s][^,]*)*\s*$", re.DOTALL)
        #checking if matching regex for correct:
        if bool(player_list_re.fullmatch(self.children[0].value)):
            players = [p.strip() for p in re.split(r'\s*,\s*', self.children[0].value.strip())]
        else:
            await interaction.response.send_message("Cannot generate team, given incorrect player format", ephemeral=True)
            return
        if not (self.children[1].value.isdigit() and int(self.children[1].value) >= 2):
            await interaction.response.send_message("Cannot generate team, given incorrect number of teams", ephemeral=True)
            return

        view = TeamGeneration("| Team Generation Ready! If you want to regenerate another "
                       "permutation, press the generation button again", players, int(self.children[1].value))
        await interaction.response.send_message("| Team Generation Ready! If you want to regenerate another permutation, "
                                                "press the generation button again", view=view)
        await view.wait()

        if view.exit_triggered:
            return


class RandomTeamMain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def generate_random_team(self, ctx):
        modal = PlayersModal(title="Team Generator")
        await ctx.send_modal(modal)

    @discord.slash_command()
    async def generate_random_team_open(self, ctx):
        max_slots = 20

        # variables
        players = max_slots * [""]

        views = [PlayerJoin("| Waiting for Players...", players),
                 TeamSettings("| Team Settings...", players),
                 None]

        await ctx.respond("| Starting Random Team Generator")

        iterator = 0
        for view in views:
            await ctx.send(content=view.message_str, view=view)
            await view.wait()

            if view.exit_triggered:
                break
            if iterator == 0:
                while "" in players:
                    players.remove("")
            if iterator == 1:
                num_teams = views[1].teams_choice
                team_generator = TeamGeneration("| Team Generation Ready! If you want to regenerate another "
                                                "permutation, press the generation button again", players, num_teams)
                views[iterator+1] = team_generator
            iterator += 1


def setup(bot):
    bot.add_cog(RandomTeamMain(bot))
