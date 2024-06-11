import discord


def button_setup(button, name, num, players):

    if button.style != discord.ButtonStyle.success:
        # checking to see if player already is registered
        if not (name in players):
            button.style = discord.ButtonStyle.success
            button.label = name

            # adding player
            players[num - 1] = name

    else:
        if name == players[num - 1]:
            button.style = discord.ButtonStyle.secondary
            button.label = f"Slot {num}"

            # setting slot to 0
            players[num - 1] = 0
