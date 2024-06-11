import discord
from ui.views.BaseView import BaseView
import cogs.helper.rushH as Helper


class PlayerJoin(BaseView):
    def __init__(self, players: list):
        super().__init__()
        self.players = players

    @discord.ui.button(label="Slot 1", style=discord.ButtonStyle.secondary, row=0)
    async def slot1_callback(self, button, interaction):
        Helper.button_setup(button, str(interaction.user), 1, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 2", style=discord.ButtonStyle.secondary, row=0)
    async def slot2_callback(self, button, interaction):
        Helper.button_setup(button, str(interaction.user), 2, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 3", style=discord.ButtonStyle.secondary, row=0)
    async def slot3_callback(self, button, interaction):
        Helper.button_setup(button, str(interaction.user), 3, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 4", style=discord.ButtonStyle.secondary, row=0)
    async def slot4_callback(self, button, interaction):
        Helper.button_setup(button, str(interaction.user), 4, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Start Game", style=discord.ButtonStyle.primary, row=1)
    async def start_game_callback(self, button, interaction):
        self.disable_all_items()

        players_str = 'Players: '
        for name in self.players:
            # empty slot == 0
            if name != 0:
                players_str += f'{name}, '

        # start of next views, switch self to next menu, problem with edit_message, need to change views
        await interaction.response.send_message(players_str)