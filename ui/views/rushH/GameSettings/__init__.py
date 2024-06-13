import discord
from ui.views.BaseView import BaseView
import cogs.helper.rushH.helper_funcs as helper

NUM_CHOICES = 3


class GameSettings(BaseView):
    def __init__(self, message: str, player: list):
        super().__init__(message, player)
        self.__players_ready = []
        self.game_choice = None
        self.mode_choice = None
        self.score_choice = None
        self.__choices_made = NUM_CHOICES * [False]

    @discord.ui.select(
        placeholder="Game (Nothing Selected)",
        min_values=1,
        max_values=1,
        row=0,
        options=[
            discord.SelectOption(
                label="Elden Ring"
            ),
            discord.SelectOption(
                label="Hollow Knight"
            ),
            discord.SelectOption(
                label="Super Mario 64"
            )
        ]
    )
    async def game_choice_callback(self, select, interaction):
        self.game_choice = select.values[0]
        self.__choices_made[0] = True
        await interaction.response.send_message(f"Player '{str(interaction.user)}' chose game: '{self.game_choice}'",
                                                delete_after=3)

    @discord.ui.select(
        placeholder="Game Mode (Nothing Selected)",
        min_values=1,
        max_values=1,
        row=1,
        options=[
            discord.SelectOption(
                label="Public Bounty",
                description="Complete public bounties first"
            ),
            discord.SelectOption(
                label="Private Bounty",
                description="Complete an private bounty quest line first"
            ),
            discord.SelectOption(
                label="Hybrid Bounties",
                description="Complete private bounties first"
            )
        ]
    )
    async def mode_choice_callback(self, select, interaction):
        self.mode_choice = select.values[0]
        self.__choices_made[1] = True
        await interaction.response.send_message(f"Player '{str(interaction.user)}' chose mode: '{self.mode_choice}'",
                                                delete_after=3)

    @discord.ui.select(
        placeholder="Score to Win (Nothing Selected)",
        min_values=1,
        max_values=1,
        row=2,
        options=[
            discord.SelectOption(
                label="1"
            ),
            discord.SelectOption(
                label="3"
            ),
            discord.SelectOption(
                label="5"
            ),
            discord.SelectOption(
                label="10"
            )
        ]
    )
    async def score_choice_callback(self, select, interaction):
        self.score_choice = int(select.values[0])
        self.__choices_made[2] = True
        await interaction.response.send_message(f"Player '{str(interaction.user)}' chose score: '{self.score_choice}'",
                                                delete_after=3)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary, row=3)
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
            self.disable_all_items()
            await interaction.response.edit_message(view=self)
            self.stop()
        else:
            await interaction.response.send_message("Please select a choice from each section and try again",
                                                    delete_after=5)
