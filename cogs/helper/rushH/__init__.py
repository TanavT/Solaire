import discord
from ui.views.rushH.gameViews.EldenRing import EldenRing


def button_setup(button, name: str, num: int, players: list[str]):

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
            players[num - 1] = ""


def lookup_game_view(game_name: str, game_choices: list[str]):
    match game_name:
        case "Elden Ring":
            return EldenRing("Elden Ring Settings...")
        case "Hollow Knight":
            pass
        case "Super Mario 64":
            pass
