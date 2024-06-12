import discord
from ui.views.BaseView import BaseView

NUM_CHOICES = 3


class GameSettings(BaseView):
    def __init__(self, message: str):
        super().__init__(message)
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
        await interaction.response.defer()

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
        await interaction.response.defer()

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
        await interaction.response.defer()

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary, row=3)
    async def next_callback(self, button, interaction):
        # since list gets changed as choices are made, there will be no starting 0 if all choices are made
        if 0 not in self.__choices_made:
            self.disable_all_items()
            await interaction.response.edit_message(view=self)
            self.stop()
        else:
            await interaction.response.send_message("Please select a choice from each section and try again")
