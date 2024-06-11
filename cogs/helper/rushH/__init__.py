import discord

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