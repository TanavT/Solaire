import discord
from ui.views.BaseView import BaseView
import random


class RunningGame(BaseView):
    def __init__(self, message: str, players: list, goal_list: list, pattern_choice: str,
                 color: discord.Color, max_score: str, game_mode: str):
        super().__init__(message, players, None)
        self.goal_list = goal_list
        self.__goal_num = 0
        self.color = color
        self.pattern = pattern_choice
        self.__possible_goals = []
        self.max_score = int(max_score)
        self.game_mode = game_mode
        self.player_and_scores = []
        for player in players:
            self.player_and_scores += [[player, 0]]

    def get_embed(self, goal_name: str, goal_region: str, goal_location: str, goal_url: str):
        embed = discord.Embed(
            title=f"Goal #{self.__goal_num}: {goal_name}",
            description=self.pattern,
            color=self.color  # Pycord provides a class with default colors you can choose from
        )
        for player in self.player_and_scores:
            embed.add_field(name="Player | Score", value=f"{player[0]} | {player[1]}", inline=False)

        embed.set_footer(text=f"{goal_location}, {goal_region}")
        embed.set_author(name="Solaire of Astora")
        embed.set_image(url=goal_url)
        return embed

    async def game_end(self, interaction: discord.Interaction):
        winner = self.player_and_scores[0]
        for player in self.player_and_scores:
            if player[1] > winner[1]:
                winner = player
        self.clear_items()
        await interaction.response.edit_message(content=f"| {winner[0]} wins with {winner[1]} points!", embed=None,
                                                view=self)
        self.stop()
        # await interaction.response.send_message(f"{winner[0]} wins with {winner[1]} points!")

    @discord.ui.button(label="get_next", custom_id="next_running_game",  style=discord.ButtonStyle.secondary, row=3)
    async def get_next(self, button, interaction):
        if self.__goal_num != 0:
            scoring_player = str(interaction.user)
            for player in self.player_and_scores:
                if player[0] == scoring_player:
                    player[1] += 1
                    if player[1] == self.max_score:
                        await self.game_end(interaction)
                        return
            if self.__goal_num == len(self.goal_list):
                await self.game_end(interaction)
                return

        if self.__goal_num == 0:
            self.__possible_goals = list(range(0, len(self.goal_list) - 1))
        self.__goal_num += 1
        new_goal = self.__possible_goals[random.randint(0, len(self.__possible_goals) - 1)]
        self.__possible_goals.remove(new_goal)

        new_embed = self.get_embed(self.goal_list[new_goal]["name"], self.goal_list[new_goal]["region"],
                                   self.goal_list[new_goal]["location"], self.goal_list[new_goal]["image"])
        await interaction.response.edit_message(embed=new_embed, view=self)
