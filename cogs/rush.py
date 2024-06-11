import discord
from discord.ext import commands
import cogs.helper.rushH as Helper

players = []
MAX_SLOTS = 4


# Start of Views
class GameSettings(discord.ui.View):
    @discord.ui.select(
        placeholder="Pick a game",
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
                label="Mario 64"
            )
        ]
    )
    async def select_callback(self, select, interaction):
        await interaction.response.send_message(f"You picked {select.values[0]}")


class PlayerJoin(discord.ui.View):
    global players

    @discord.ui.button(label="Slot 1", style=discord.ButtonStyle.secondary, row=0)
    async def slot1_callback(self, button, interaction):
        Helper.button_setup(button, str(interaction.user), 1, players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 2", style=discord.ButtonStyle.secondary, row=0)
    async def slot2_callback(self, button, interaction):
        Helper.button_setup(button, str(interaction.user), 2, players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 3", style=discord.ButtonStyle.secondary, row=0)
    async def slot3_callback(self, button, interaction):
        Helper.button_setup(button, str(interaction.user), 3, players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 4", style=discord.ButtonStyle.secondary, row=0)
    async def slot4_callback(self, button, interaction):
        Helper.button_setup(button, str(interaction.user), 4, players)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Start Game", style=discord.ButtonStyle.primary, row=1)
    async def start_game_callback(self, button, interaction):
        self.disable_all_items()

        players_str = 'Players: '
        for name in players:

            # empty slot == 0
            if name != 0:
                players_str += f'{name}, '

        # start of next view, switch self to next menu, problem with edit_message, need to change view
        await interaction.response.send_message(players_str)

        # await interaction.response.edit_message(view=self)


# Start of cog class
class RushMain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def rush(self, ctx):
        global players
        global MAX_SLOTS

        players = MAX_SLOTS * [0]
        await ctx.respond("Waiting for Players...", view=PlayerJoin())


def setup(bot):
    bot.add_cog(RushMain(bot))
