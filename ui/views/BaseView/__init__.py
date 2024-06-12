import discord


class BaseView (discord.ui.View):
    # add timeout later
    def __init__(self, message: str):
        super().__init__()
        self.message = message
        self.exit_triggered = False

    @discord.ui.button(label="Exit", style=discord.ButtonStyle.danger, row=4)
    async def exit_callback(self, button, interaction):
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        self.exit_triggered = True
        self.stop()

    async def on_error(self, error, item, interaction):
        await interaction.response.send_message(f'Error: {str(error)}')
