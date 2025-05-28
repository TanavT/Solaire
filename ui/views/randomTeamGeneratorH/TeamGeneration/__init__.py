import discord
import random

from ui.views.BaseView import BaseView

NUM_CHOICES = 1
class TeamGeneration(BaseView):

    def __init__(self, message_str: str, players: list, num_teams: int):
        super().__init__(message_str, players, 300)
        self.__num_teams = num_teams
        self.__number_generations = 0

    def generate_random_teams(self):
        self.__number_generations += 1
        teams = [[] for _ in range(self.__num_teams)]
        random.shuffle(self.players)
        for i in range(len(self.players)):
            teams[i % self.__num_teams] += [self.players[i]]
        return self.get_embed(teams)
    def get_embed(self, teams):
        embed = discord.Embed(
            title=f"Teams Generator",
            description=f"Dividing {len(self.players)} players into {self.__num_teams} teams",
            color= discord.Color.blurple()
        )
        for team_num in range(len(teams)):
            embed.add_field(name=f"Team #{team_num + 1}", value=f"{teams[team_num]}", inline=True)

        embed.set_footer(text=f"Number of Generation: {self.__number_generations}")
        embed.set_author(name="Solaire of Astora")
        return embed


    @discord.ui.button(label="Generate", custom_id="generate_random_team_generation", style=discord.ButtonStyle.primary, row=4)
    async def generate_callback(self, button, interaction):
        embed_teams = self.generate_random_teams()
        await interaction.response.edit_message(view=self, embed = embed_teams)
