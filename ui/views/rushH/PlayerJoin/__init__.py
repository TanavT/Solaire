import discord
from ui.views.BaseView import BaseView
import cogs.helper.rushH.helper_funcs as helper


class PlayerJoin(BaseView):
    def __init__(self, message: str, players: list):
        super().__init__(message, players)

    @discord.ui.button(label="Slot 1", style=discord.ButtonStyle.secondary, row=0)
    async def slot1_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 1, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 2", style=discord.ButtonStyle.secondary, row=0)
    async def slot2_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 2, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 3", style=discord.ButtonStyle.secondary, row=0)
    async def slot3_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 3, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 4", style=discord.ButtonStyle.secondary, row=0)
    async def slot4_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 4, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary, row=1)
    async def next_callback(self, button, interaction):
        for playerI in range(len(self.players)):
            # will break if at least one slot is filled
            if self.players[playerI] != "":
                break

            if playerI == len(self.players) - 1:
                await interaction.response.send_message("No players found, cannot start game yet",
                                                        delete_after=5)
                return

        self.disable_all_items()

        players_str = 'Players: '
        for name in self.players:
            # empty slot == ""
            if name != "":
                players_str += f'{name}, '

        # start of next views, switch self to next menu, problem with edit_message, need to change views
        await interaction.response.edit_message(view=self)
        self.stop()
