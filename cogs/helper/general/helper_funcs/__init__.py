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

    if len(players_ready) < (player_count + 1)//2:
        return False, True

    return False, False


# used in running games
def convert_seconds_to_clock(time_to_convert):
    clock_string = ""

    hours = int(time_to_convert/3600)
    # multiplication instead of modulo for purpose of efficiency
    minutes = int((time_to_convert - hours * 3600)/60)
    seconds = int(time_to_convert - hours * 3600 - minutes * 60)

    if hours > 0:
        hours_str = str(hours).zfill(2)
        clock_string += f"{hours_str}:"
    minutes_str = str(minutes).zfill(2)
    clock_string += f"{minutes_str}:"
    seconds_str = f"{seconds:d}".zfill(2)
    clock_string += f"{seconds_str}"

    # print(f"{hours}, {minutes}, {seconds}")
    return clock_string


def convert_clock_to_seconds(clock_to_convert):
    times = clock_to_convert.split(":")

    # multiplied by 60 everytime we move from seconds -> minutes -> hours
    # does not work with days, unless we check to see if we are converting from hours -> days
    current_power = 1
    sum_time_in_seconds = 0

    for index in range(len(times)-1, -1, -1):
        sum_time_in_seconds += int(times[index]) * current_power
        current_power *= 60

    return sum_time_in_seconds

