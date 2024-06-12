import discord
from discord.ext import commands
import requests

class PlayerJoinView(discord.ui.View):
    @discord.ui.button(label="Slot 1", style=discord.ButtonStyle.secondary, row=0)
    async def slot1_callback(self, button, interaction):
        if button.style != discord.ButtonStyle.success:
            button.style = discord.ButtonStyle.success
            button.label = str(interaction.user)
        else:
            button.style = discord.ButtonStyle.secondary
            button.label = "Slot 1"
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 2", style=discord.ButtonStyle.secondary, row=0)
    async def slot2_callback(self, button, interaction):
        if button.style != discord.ButtonStyle.success:
            button.style = discord.ButtonStyle.success
            button.label = str(interaction.user)
        else:
            button.style = discord.ButtonStyle.secondary
            button.label = "Slot 2"
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 3", style=discord.ButtonStyle.secondary, row=0)
    async def slot3_callback(self, button, interaction):
        if button.style != discord.ButtonStyle.success:
            button.style = discord.ButtonStyle.success
            button.label = str(interaction.user)
        else:
            button.style = discord.ButtonStyle.secondary
            button.label = "Slot 3"
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 4", style=discord.ButtonStyle.secondary, row=0)
    async def slot4_callback(self, button, interaction):
        if button.style != discord.ButtonStyle.success:
            button.style = discord.ButtonStyle.success
            button.label = str(interaction.user)
        else:
            button.style = discord.ButtonStyle.secondary
            button.label = "Slot 4"
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Start Game", style=discord.ButtonStyle.primary, row=1)
    async def start_game_callback(self, interaction):
        self.disable_all_items()
        await interaction.response.edit_message(view=self)


class TestingSpaceClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def greetings(self, ctx):
        await ctx.respond('Greetings!')

    @discord.user_command()
    async def person_greeting(self, ctx, member: discord.Member):
        await ctx.respond(f'{ctx.author.mention} says hello to {member.mention}')

    @discord.slash_command()
    async def player_slots(self, ctx):
        await ctx.respond("Waiting for Players...", view=PlayerJoinView())

    @discord.slash_command()
    async def api_pull(self, ctx):
        response = requests.get("https://eldenring.fanapis.com/api/graphql")
        # below broken
        print(response.json())
        await ctx.respond("api pulled")


def setup(bot):
    bot.add_cog(TestingSpaceClass(bot))
