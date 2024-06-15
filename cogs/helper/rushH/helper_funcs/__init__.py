import discord
from typing import Tuple


# used in ui.views.rushH.PlayerJoin
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


# # used in check_end_early
# def calculate_players(players: list[str]):
#     num_players = 0
#     for player in players:
#         if player != "":
#             num_players += 1
#     return num_players


# used in most views under ui.views
def check_end_early(choices_made: list, current_user: str, players: list, players_ready: list) -> Tuple[bool, bool]:
    """returns true if either end condition is met, true in fst if not enough choices,
     true in snd if not enough players"""
    player_count = len(players)
    if False in choices_made:
        return True, True  # snd doesn't matter because will return before it checks snd

    # checking if all players have confirmed
    if current_user not in players_ready and current_user in players:
        players_ready += [current_user]

    if len(players_ready) != player_count:
        return False, True

    return False, False
