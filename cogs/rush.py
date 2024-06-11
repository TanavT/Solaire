import discord
from discord.ext import commands

players = []
MAX_SLOTS = 4

#helper func
def buttonSetup(button, interaction, num):
    global players
    if button.style != discord.ButtonStyle.success:
        button.style = discord.ButtonStyle.success
        button.label = str(interaction.user)

        # adding player
        players[num - 1] = str(interaction.user)
    else:
        button.style = discord.ButtonStyle.secondary
        button.label = f"Slot {num}"

        #setting slot to 0
        players[num - 1] = 0

#Start of Views
class gameSettings(discord.ui.View):
    @discord.ui.select(
        placeholder = "Pick a game",
        min_values = 1,
        max_values = 1,
        row = 0,
        options = [
            discord.SelectOption(
                label = "Elden Ring"
            ),
            discord.SelectOption(
                label = "Hollow Knight"
            ),
            discord.SelectOption(
                label = "Mario 64"
            )
        ]
    )

    async def select_callback(self, select, interaction):
        await interaction.response.send_message(f"You picked {select.values[0]}")
class playerJoin(discord.ui.View):
    global players
    @discord.ui.button(label = "Slot 1", style = discord.ButtonStyle.secondary, row = 0)
    async def slot1_callback(self, button, interaction):
        buttonSetup(button, interaction, 1)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label = "Slot 2", style = discord.ButtonStyle.secondary, row = 0)
    async def slot2_callback(self, button, interaction):
        buttonSetup(button, interaction, 2)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label = "Slot 3", style = discord.ButtonStyle.secondary, row = 0)
    async def slot3_callback(self, button, interaction):
        buttonSetup(button, interaction, 3)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label = "Slot 4", style = discord.ButtonStyle.secondary, row = 0)
    async def slot4_callback(self, button, interaction):
        buttonSetup(button, interaction, 4)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Start Game", style=discord.ButtonStyle.primary, row=1)
    async def startGame_callback(self, button, interaction):
        self.disable_all_items()

        playersStr = 'Players: '
        for name in players:

            #empty slot == 0
            if name != 0:
                playersStr += f'{name}, '

        #start of next view, switch self to next menu, problem with edit_message, need to change view
        await interaction.response.edit_message(view=gameSettings)

#Start of cog class
class rushMain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def rush(self, ctx):
        global players
        global MAX_SLOTS

        players = MAX_SLOTS * [0]
        await ctx.respond("Waiting for Players...", view=playerJoin())

def setup(bot):
    bot.add_cog(rushMain(bot))
