import discord
from ui.views.BaseView import BaseView
import cogs.helper.rushH.helper_funcs as helper

NUM_CHOICES = 3


class GameSettings(BaseView):
    def __init__(self, message_str: str, player: list):
        super().__init__(message_str, player, 300)
        self.__players_ready = []
        self.game_choice = None
        self.length_choice = None
        self.__choices_made = NUM_CHOICES * [False]

    @discord.ui.select(
        placeholder="Game",
        min_values=1,
        max_values=1,
        row=0,
        custom_id="game_select",
        options=[
            discord.SelectOption(
                label="Elden Ring"
            ),
            discord.SelectOption(
                label="Hollow Knight"
            ),
            discord.SelectOption(
                label="Super Mario Odyssey"
            )
        ]
    )
    async def game_choice_callback(self, select, interaction):
        self.game_choice = select.values[0]
        self.__choices_made[0] = True
        await self.update_settings(interaction, self.game_choice, self.length_choice)
        # await interaction.response.send_message(f"Player '{str(interaction.user)}' chose game: '{self.game_choice}'",
        #                                         delete_after=3)

    @discord.ui.select(
        placeholder="Game Length",
        min_values=1,
        max_values=1,
        row=1,
        custom_id="length_select_race",
        options=[
            discord.SelectOption(
                label="Early Game",
                description="Early game area or goal, probably around 0-1 hour to complete"
            ),
            discord.SelectOption(
                label="Mid Game",
                description="Mid game area or goal, probably around 2-3 hours to complete"
            ),
            discord.SelectOption(
                label="Late Game",
                description="Late game area or goal, probably probably 3+ hours to complete"
            )
        ]
    )
    async def length_choice_callback(self, select, interaction):
        self.length_choice = select.values[0]
        self.__choices_made[1] = True
        await self.update_settings(interaction, self.game_choice, self.length_choice)

        # await interaction.response.send_message(f"Player '{str(interaction.user)}' chose mode:'{self.length_choice}'",
        #                                         delete_after=3)

    @discord.ui.button(label="Next", custom_id="next_game_settings", style=discord.ButtonStyle.primary, row=4)
    async def next_callback(self, button, interaction):
        # since list gets changed as choices are made, there will be no starting 0 if all choices are made
        current_user = str(interaction.user)
        end_conditions = helper.check_end_early(self.__choices_made, current_user, self.players, self.__players_ready)
        # checking if all choices were made
        if end_conditions[0]:
            await interaction.response.send_message("Please select a choice from each section and try again",
                                                    delete_after=5)
            return

        if end_conditions[1]:
            await interaction.response.send_message(f"Player {current_user} has readied;"
                                                    f" {len(self.__players_ready)} players ready.",
                                                    delete_after=5)
            return

        if 0 not in self.__choices_made:
            self.clear_items()
            await interaction.response.edit_message(content=f"| Game Settings:\n"
                                                            f"  Game = {self.game_choice}\n"
                                                            f"  Game Length = {self.length_choice}\n",
                                                    view=self)
            self.stop()
        else:
            await interaction.response.send_message("Please select a choice from each section and try again",
                                                    delete_after=5)
