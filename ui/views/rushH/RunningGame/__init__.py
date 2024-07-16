import discord
from ui.views.BaseView import BaseView
import random
# from discord.ui import Button
import math
import time
import cogs.helper.rushH.helper_funcs as helper


class RunningGame(BaseView):
    def __init__(self, message_str: str, players: list, goal_list: list, pattern_choice: str,
                 color: discord.Color, max_score: str, game_mode: str, goal_choices: list, setup_choice: str):
        super().__init__(message_str, players, None)
        self.goal_list = goal_list
        self.__goal_num = 0
        self.color = color
        self.__point_amount = 1
        self.__possible_goals = []
        self.__goal_choices = goal_choices

        self.__game_mode = None
        if game_mode == "Public Bounties":
            self.__game_mode = 0
        elif game_mode == "Private Bounty List":
            self.__game_mode = 1
        elif game_mode == "Hybrid Bounties":
            self.__game_mode = 2
        else:
            raise ValueError("Unknown Bounty Choice")

        if max_score == "No Limit":
            self.max_score = math.inf
            self.goals_percent_reciprocal = 1.0
        else:
            self.max_score = int(max_score)
            self.goals_percent_reciprocal = len(self.goal_list) / ((self.max_score - 1) * len(players) + 1)
            if self.goals_percent_reciprocal < 1.0:
                self.goals_percent_reciprocal = 1.0

        self.ramping = False
        self.pattern = pattern_choice.split(" & ")
        if len(self.pattern) > 1 and self.pattern[1] == "Ramping":
            self.ramping = True
        if self.pattern[0] == "Random Choice":
            self.pattern = 0
        elif self.pattern[0] == "Progressive Choice":
            self.pattern = 1
        else:
            raise ValueError("Unknown pattern choice")

        self.__setup_choice = setup_choice
        self.__started_setup = False
        self.__start_time = None

        self.player_and_scores = []
        for player in players:
            self.player_and_scores += [[player, 0]]

    # Next Button
    @discord.ui.button(label="Start!", custom_id="running_game",  style=discord.ButtonStyle.primary, row=3)
    async def next_callback(self, button, interaction):
        await self.get_next(button, interaction, True)

    # Skip Button
    async def skip_callback(self, interaction):
        await self.get_next(None, interaction, False)

    async def get_next(self, button, interaction, award_point: bool):
        if self.__goal_num != 0:
            scoring_player = str(interaction.user)
            if award_point:
                for player in self.player_and_scores:
                    if player[0] == scoring_player:
                        player[1] += self.__point_amount
                        if player[1] >= self.max_score:
                            await self.game_end(interaction)
                            return
            if self.__goal_num == len(self.goal_list):
                await self.game_end(interaction)
                return

        if self.__goal_num == 0:
            if self.__setup_choice != 0:
                if not self.__started_setup:
                    self.__start_time = time.time()
                    self.__started_setup = True

                current_time = time.time()
                if current_time - self.__start_time < self.__setup_choice:
                    button.label = (f"Setup Time Remaining: {helper.convert_seconds_to_clock(
                        self.__setup_choice - (current_time - self.__start_time))}"
                                    f" (Click to Update)")
                    await interaction.response.edit_message(view=self)
                    return

            self.__possible_goals = list(range(0, len(self.goal_list)))
            button.label = "Finished!"
            # skip_button = discord.ui.button(label="Skip", custom_id="skip_button",
            #                                 style=discord.ButtonStyle.secondary, row=3)
            # skip_button.callback = skip_button
            # self.add_item(skip_button)

        new_goal = self.get_next_goal()

        new_embed = self.get_embed(self.goal_list[new_goal]["name"], self.goal_list[new_goal]["region"],
                                   self.goal_list[new_goal]["location"], self.goal_list[new_goal]["image"])

        await interaction.response.edit_message(view=self, embed=new_embed)

    def get_next_goal(self) -> str:
        if self.ramping:
            self.__point_amount = int(self.__goal_num / 3) + 1

        new_goal = None
        if self.pattern == 0:
            new_goal = self.__possible_goals[random.randint(0, len(self.__possible_goals) - 1)]
        if self.pattern == 1:
            if self.max_score == math.inf:
                new_goal = self.__possible_goals[0]
            else:
                # subtraction accounting for value being removed from list in every case except first
                new_goal_start_index = int(self.__goal_num * self.goals_percent_reciprocal - self.__goal_num)
                new_goal_end_index = int(((self.__goal_num + 1) * self.goals_percent_reciprocal) - (self.__goal_num + 1))

                new_goal = self.__possible_goals[random.randint(new_goal_start_index, new_goal_end_index)]

        self.__possible_goals.remove(new_goal)
        self.__goal_num += 1
        return new_goal

    def get_embed(self, goal_name: str, goal_region: str, goal_location: str, goal_url: str):
        embed = discord.Embed(
            title=f"Goal #{self.__goal_num}:\n{goal_name}",
            description=f"{goal_location}, {goal_region}",
            color=self.color  # Pycord provides a class with default colors you can choose from
        )
        # embed.set_image(url=goal_url) # embed images take too long to pull
        for player in self.player_and_scores:
            embed.add_field(name="Player | Score", value=f"{player[0]} | {player[1]}", inline=False)

        embed.set_footer(text=f"{self.pattern} | Score to Win = {self.max_score} | This Goal's points ="
                              f" {self.__point_amount}")
        embed.set_author(name="Solaire of Astora")
        return embed

    async def game_end(self, interaction: discord.Interaction):
        winner = self.player_and_scores[0]
        for player in self.player_and_scores:
            if player[1] > winner[1]:
                winner = player
        self.clear_items()
        await interaction.response.edit_message(content=f"| {winner[0].upper()} wins with {winner[1]} points!",
                                                embed=None, view=self)
        self.stop()
        # await interaction.response.send_message(f"{winner[0]} wins with {winner[1]} points!")
