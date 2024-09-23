import discord
from ui.views.BaseView import BaseView

NUM_CHOICES = 1
class TeamSettings(BaseView):

    def __init__(self, message_str: str, player: list):
        super().__init__(message_str, player, 300)
        self.teams_choice = None
        self.__choices_made = NUM_CHOICES * [False]

    @discord.ui.select(
        placeholder="Number of Teams",
        min_values=1,
        max_values=1,
        row=0,
        custom_id="number_of_teams_random",
        options=[
            discord.SelectOption(
                label="2 Teams"
            ),
            discord.SelectOption(
                label="3 Teams"
            ),
            discord.SelectOption(
                label="4 Teams"
            ),
            discord.SelectOption(
                label="5 Teams"
            ),
            discord.SelectOption(
                label="6 Teams"
            ),
            discord.SelectOption(
                label="7 Teams"
            ),
            discord.SelectOption(
                label="8 Teams"
            ),
            discord.SelectOption(
                label="9 Teams"
            ),
            discord.SelectOption(
                label="10 Teams"
            )
        ]
    )
    async def teams_choice_callback(self, select, interaction):
        self.teams_choice = int(select.values[0][0])
        self.__choices_made[0] = True
        await self.update_settings(interaction, self.teams_choice)

    @discord.ui.button(label="Next", custom_id="next_random_team_settings", style=discord.ButtonStyle.primary, row=4)
    async def next_callback(self, button, interaction):
        if 0 not in self.__choices_made:
            self.clear_items()
            await interaction.response.edit_message(content=f"| Team Settings:\n"
                                                            f"  Number of Teams = {self.teams_choice}",
                                                    view=self)
            self.stop()
        else:
            await interaction.response.send_message("Please select a choice from each section and try again",
                                                    delete_after=5)
