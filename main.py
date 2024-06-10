from typing import Final
import os
from dotenv import load_dotenv
import discord

#loading token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

#setting up bot
bot = discord.Bot()

class playerJoinView(discord.ui.View):
    @discord.ui.button(label = "Slot 1", style = discord.ButtonStyle.secondary, row = 0)
    async def slot1_callback(self, button, interaction):
        if button.style != discord.ButtonStyle.success:
            button.style = discord.ButtonStyle.success
            button.label = str(interaction.user)
        else:
            button.style = discord.ButtonStyle.secondary
            button.label = "Slot 1"
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label = "Slot 2", style = discord.ButtonStyle.secondary, row = 0)
    async def slot2_callback(self, button, interaction):
        if button.style != discord.ButtonStyle.success:
            button.style = discord.ButtonStyle.success
            button.label = str(interaction.user)
        else:
            button.style = discord.ButtonStyle.secondary
            button.label = "Slot 2"
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label = "Slot 3", style = discord.ButtonStyle.secondary, row = 0)
    async def slot3_callback(self, button, interaction):
        if button.style != discord.ButtonStyle.success:
            button.style = discord.ButtonStyle.success
            button.label = str(interaction.user)
        else:
            button.style = discord.ButtonStyle.secondary
            button.label = "Slot 3"
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label = "Slot 4", style = discord.ButtonStyle.secondary, row = 0)
    async def slot4_callback(self, button, interaction):
        if button.style != discord.ButtonStyle.success:
            button.style = discord.ButtonStyle.success
            button.label = str(interaction.user)
        else:
            button.style = discord.ButtonStyle.secondary
            button.label = "Slot 4"
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Start Game", style=discord.ButtonStyle.primary, row=1)
    async def startGame_callback(self, button, interaction):
        self.disable_all_items()
        await interaction.response.edit_message(view=self)

@bot.slash_command()
async def speedrun(ctx):
    await ctx.respond("Waiting for Players...", view = playerJoinView())

#main entry point
def main() -> None:
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()