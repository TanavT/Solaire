import discord
from ui.views.BaseView import BaseView


class RunningGame(BaseView):
    def __init__(self, message: str, players: list, goal_list: list):
        super().__init__(message, players)
        self.goal_list = goal_list
