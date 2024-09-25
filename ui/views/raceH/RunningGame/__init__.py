import discord
from ui.views.BaseView import BaseView
import random
# from discord.ui import Button


class RunningGame(BaseView):
    def __init__(self, message_str: str, players: list, goal_list: list, color: discord.Color
                 , game: str, game_length: str):
        super().__init__(message_str, players, None)
        self.__goal_list = goal_list
        self.color = color
        self.game = game
        self.game_length = game_length

    @discord.ui.button(label="Start!", custom_id="running_game_race", style=discord.ButtonStyle.primary, row=4)
    async def next_callback(self, button, interaction):
        if button.label == "Start!":
            button.label = "Finished!"

            goal = random.randint(0, len(self.__goal_list))
            embed = discord.Embed(
                title=self.__goal_list[goal]["name"],
                description=f"{self.__goal_list[goal]['location']}, {self.__goal_list[goal]['region']}",
                color=self.color  # Pycord provides a class with default colors you can choose from
            )
            # embed.set_image(url=goal_url) # embed images take too long to pull
            for player in self.players:
                embed.add_field(name="Player", value=f"{player}", inline=False)

            embed.set_footer(text=f"Game = {self.game} | First to complete this goal wins!")
            embed.set_author(name="Solaire of Astora")
            await interaction.response.edit_message(view=self, embed=embed)
        else:
            self.clear_items()
            game_over_str = f"| Game Over! Winner: {interaction.user}"
            await interaction.response.edit_message(content=game_over_str, embed=None, view=self)
            self.stop()
