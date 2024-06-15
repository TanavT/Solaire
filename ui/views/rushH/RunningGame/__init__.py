import discord
from ui.views.BaseView import BaseView
import random


class RunningGame(BaseView):
    def __init__(self, message: str, players: list, goal_list: list, pattern_choice: str, color: discord.Color):
        super().__init__(message, players)
        self.goal_list = goal_list
        self.__goal_num = 0
        self.color = color
        self.pattern = pattern_choice
        self.__past_goals = [-1]
        print("got to initialization")

    def get_embed(self, goal_name: str, goal_region: str, goal_location: str, goal_url: str):
        embed = discord.Embed(
            title=f"Goal #{self.__goal_num}: {goal_name}",
            description=self.pattern,
            color=self.color  # Pycord provides a class with default colors you can choose from
        )
        embed.add_field(name="Player 1 | Score", value="Inline Field 1", inline=False)
        embed.add_field(name="Player 2 | Score", value="Inline Field 2", inline=False)
        embed.add_field(name="Player 3 | Score", value="Inline Field 3", inline=False)
        embed.add_field(name="Player 4 | Score", value="Inline Field 4", inline=False)

        embed.set_footer(text=f"{goal_location}, {goal_region}")
        embed.set_author(name="Solaire of Astora")
        embed.set_image(url=goal_url)
        return embed

    @discord.ui.button(label="get_next", style=discord.ButtonStyle.secondary, row=3)
    async def get_next(self, button, interaction):
        print("got to the start of get_next")
        self.__goal_num += 1
        new_goal = -1
        print("got before new_goal")
        while new_goal in self.__past_goals:
            new_goal = random.randint(1, len(self.goal_list))
        self.__past_goals += [new_goal]
        print("Got before embed")
        new_embed = self.get_embed(self.goal_list[new_goal]["name"], self.goal_list[new_goal]["region"],
                                   self.goal_list[new_goal]["location"], self.goal_list[new_goal]["image"])
        print("Got after embed")
        await interaction.response.edit_message(embed=new_embed, view=self)
