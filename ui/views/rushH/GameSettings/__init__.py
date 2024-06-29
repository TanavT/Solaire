import discord
from ui.views.BaseView import BaseView
import cogs.helper.rushH.helper_funcs as helper

NUM_CHOICES = 4


class GameSettings(BaseView):
    def __init__(self, message_str: str, player: list):
        super().__init__(message_str, player, 300)
        self.__players_ready = []
        self.game_choice = None
        self.mode_choice = None
        self.score_choice = None
        self.setup_choice = None
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
        await self.update_settings(interaction, self.game_choice, self.mode_choice,
                                   self.score_choice, self.setup_choice)
        # await interaction.response.send_message(f"Player '{str(interaction.user)}' chose game: '{self.game_choice}'",
        #                                         delete_after=3)

    @discord.ui.select(
        placeholder="Game Mode",
        min_values=1,
        max_values=1,
        row=1,
        custom_id="bounty_select",
        options=[
            discord.SelectOption(
                label="Public Bounties",
                description="Complete public bounties first"
            ),
            discord.SelectOption(
                label="Private Bounty List",
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
        await self.update_settings(interaction, self.game_choice, self.mode_choice,
                                   self.score_choice, self.setup_choice)
        # await interaction.response.send_message(f"Player '{str(interaction.user)}' chose mode: '{self.mode_choice}'",
        #                                         delete_after=3)

    @discord.ui.select(
        placeholder="Score to Win",
        min_values=1,
        max_values=1,
        row=2,
        custom_id="score_select",
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
            ),
            discord.SelectOption(
                label="20"
            ),
            discord.SelectOption(
                label="35"
            ),
            discord.SelectOption(
                label="50"
            ),
            discord.SelectOption(
                label="75"
            ),
            discord.SelectOption(
                label="100"
            ),
            discord.SelectOption(
                label="No Limit"
            )
        ]
    )
    async def score_choice_callback(self, select, interaction):
        self.score_choice = select.values[0]
        self.__choices_made[2] = True
        await self.update_settings(interaction, self.game_choice, self.mode_choice,
                                   self.score_choice, self.setup_choice)
        # await interaction.response.send_message(f"Player '{str(interaction.user)}' "
        #                                         f"chose score: '{self.score_choice}'",
        #                                         delete_after=3)

    @discord.ui.select(
        placeholder="Setup Period",
        min_values=1,
        max_values=1,
        row=3,
        custom_id="setup_period_select",
        options=[
            discord.SelectOption(
                label="None",
                description="Goals are displayed at game start"
            ),
            discord.SelectOption(
                label="1 Minute",
                description="Goals are displayed 1 minute after game start"
            ),
            discord.SelectOption(
                label="5 Minutes",
                description="Goals are displayed 5 minutes after game start"
            ),
            discord.SelectOption(
                label="10 Minutes",
                description="Goals are displayed 10 minutes after game start"
            ),
            discord.SelectOption(
                label="15 Minutes",
                description="Goals are displayed 15 minutes after game start"
            ),
            discord.SelectOption(
                label="20 Minute",
                description="Goals are displayed 20 minutes after game start"
            ),
            discord.SelectOption(
                label="30 Minutes",
                description="Goals are displayed 30 minutes after game start"
            ),
            discord.SelectOption(
                label="45 Minutes",
                description="Goals are displayed 45 minutes after game start"
            ),
            discord.SelectOption(
                label="1 Hour",
                description="Goals are displayed 1 hour after game start"
            )
        ]
    )
    async def setup_choice_callback(self, select, interaction):
        self.setup_choice = select.values[0]
        self.__choices_made[3] = True
        await self.update_settings(interaction, self.game_choice, self.mode_choice,
                                   self.score_choice, self.setup_choice)

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
                                                            f"  Game Mode = {self.mode_choice}\n"
                                                            f"  Score to Win = {self.score_choice}",
                                                    view=self)
            self.stop()
        else:
            await interaction.response.send_message("Please select a choice from each section and try again",
                                                    delete_after=5)
