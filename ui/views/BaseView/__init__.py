import discord


class BaseView (discord.ui.View):
    def __init__(self):
        super().__init__()

    async def on_error(self, error, item, interaction):
        await interaction.response.send_message(f'Error: {str(error)}')
