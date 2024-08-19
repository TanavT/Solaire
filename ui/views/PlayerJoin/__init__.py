import discord
from ui.views.BaseView import BaseView
import cogs.helper.rushH.helper_funcs as helper


class PlayerJoin(BaseView):
    def __init__(self, message_str: str, players: list):
        super().__init__(message_str, players, 300)

# row 0
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

    @discord.ui.button(label="Slot 5", style=discord.ButtonStyle.secondary, row=0)
    async def slot5_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 5, self.players)
        await interaction.response.edit_message(view=self)

# row 1
    @discord.ui.button(label="Slot 6", style=discord.ButtonStyle.secondary, row=1)
    async def slot6_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 6, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 7", style=discord.ButtonStyle.secondary, row=1)
    async def slot7_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 7, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 8", style=discord.ButtonStyle.secondary, row=1)
    async def slot8_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 8, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 9", style=discord.ButtonStyle.secondary, row=1)
    async def slot9_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 9, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 10", style=discord.ButtonStyle.secondary, row=1)
    async def slot10_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 10, self.players)
        await interaction.response.edit_message(view=self)

# row 2
    @discord.ui.button(label="Slot 11", style=discord.ButtonStyle.secondary, row=2)
    async def slot11_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 11, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 12", style=discord.ButtonStyle.secondary, row=2)
    async def slot12_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 12, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 13", style=discord.ButtonStyle.secondary, row=2)
    async def slot13_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 13, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 14", style=discord.ButtonStyle.secondary, row=2)
    async def slot14_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 14, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 15", style=discord.ButtonStyle.secondary, row=2)
    async def slot15_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 15, self.players)
        await interaction.response.edit_message(view=self)

# row 3
    @discord.ui.button(label="Slot 16", style=discord.ButtonStyle.secondary, row=3)
    async def slot16_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 16, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 17", style=discord.ButtonStyle.secondary, row=3)
    async def slot17_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 17, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 18", style=discord.ButtonStyle.secondary, row=3)
    async def slot18_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 18, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 19", style=discord.ButtonStyle.secondary, row=3)
    async def slot19_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 19, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 20", style=discord.ButtonStyle.secondary, row=3)
    async def slot20_callback(self, button, interaction):
        helper.button_setup(button, str(interaction.user), 20, self.players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Next", custom_id="next_player_join", style=discord.ButtonStyle.primary, row=4)
    async def next_callback(self, button, interaction):
        for playerI in range(len(self.players)):
            # will break if at least one slot is filled
            if self.players[playerI] != "":
                break

            if playerI == len(self.players) - 1:
                await interaction.response.send_message("No players found, cannot start game yet",
                                                        delete_after=5)
                return

        self.clear_items()

        players_str = 'Players: '
        for name in self.players:
            # empty slot == ""
            if name != "":
                players_str += f'{name}, '

        players_str = players_str[:-2]

        # start of next views, switch self to next menu, problem with edit_message, need to change views
        await interaction.response.edit_message(content=f"| Players = {players_str}", view=self)
        self.stop()
