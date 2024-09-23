import discord
import cogs.helper.general.helper_funcs as helper


class BaseView (discord.ui.View):
    # add timeout later
    def __init__(self, message_str: str, players: list, time_on=300):
        super().__init__(timeout=time_on)
        self.__players_ready = []
        self.players = players
        self.message_str = message_str
        self.exit_triggered = False

    async def update_settings(self, interaction, *argv):
        setting_str = str(self.message_str) + "  "
        for arg in argv:
            if arg is None:
                continue
            setting_str += str(arg) + '; '
        await interaction.response.edit_message(view=self, content=setting_str[:-2])

    @discord.ui.button(label="Exit", style=discord.ButtonStyle.danger, row=4)
    async def exit_callback(self, button, interaction):
        current_user = str(interaction.user)
        end_conditions = helper.check_end_early([], current_user, self.players, self.__players_ready)

        if end_conditions[1]:
            await interaction.response.send_message(f"Player {current_user} has voted to exit;"
                                                    f" {len(self.__players_ready)} players have voted to exit.",
                                                    delete_after=8)
            return

        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        self.exit_triggered = True
        self.stop()

    async def on_timeout(self):
        self.disable_all_items()
        self.exit_triggered = True
        self.stop()

    # async def on_error(self, error, item, interaction):
    #     await interaction.response.send_message(f'Error: {str(error)}')
