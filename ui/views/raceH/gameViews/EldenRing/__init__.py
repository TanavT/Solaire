import discord
from ui.views.BaseView import BaseView
import json
import requests
import cogs.helper.general.helper_funcs as helper

NUM_CHOICES = 2
# pulls from elden_ring database, elden ring api needs to be running during this
QUERY_URL = "http://localhost:3000/api/graphql"


# output is list of goals found in goal_list, contains name, image, region, location, and difficulty
class EldenRing(BaseView):
    def __init__(self, message_str: str, player: list, length: str):
        super().__init__(message_str, player, 300)
        self.__players_ready = []
        self.goal_choices = None

        if length == "Early Game":
            self.difficulty_choice = range(1, 19)
        elif length == "Mid Game":
            self.difficulty_choice = range(19, 37)
        elif length == "Late Game":
            self.difficulty_choice = range(37, 53)
        self.__important_only = None
        self.goal_list = []
        self.__choices_made = NUM_CHOICES * [False]
        self.color = discord.Color.gold()

    @discord.ui.select(
        placeholder="Goal",
        min_values=1,
        max_values=3,
        row=0,
        options=[
            discord.SelectOption(
                label="Boss",
            ),
            discord.SelectOption(
                label="Locations",
            ),
            discord.SelectOption(
                label="Runes",
            )
        ]
    )
    async def goal_choice_callback(self, select, interaction):
        self.__choices_made[0] = True
        self.goal_choices = []
        for goal in select.values:
            self.goal_choices += [goal.lower()]
        await self.update_settings(interaction, self.goal_choices, self.__important_only)
        # await interaction.response.send_message(f"Player '{str(interaction.user)}' chose goals: "
        #                                         f"'{self.goal_choices}'",
        #                                         delete_after=3)

    @discord.ui.select(
        placeholder="Important Goals Only?",
        min_values=1,
        max_values=1,
        row=3,
        options=[
            discord.SelectOption(
                label="Yes",
                description="Only Major Goals in Game can be selected (ex. Remembrance Bosses) ",
            ),
            discord.SelectOption(
                label="No",
                description="Any Goal in Game can be selected",
            )
        ]
    )
    async def important_choice_callback(self, select, interaction):
        self.__important_only = select.values[0]
        self.__choices_made[1] = True
        await self.update_settings(interaction, self.goal_choices, self.__important_only)
        # await interaction.response.send_message(f"Player '{str(interaction.user)}' chose goals: "
        #                                         f"'{self.goal_choices}'",
        #                                         delete_after=3)

    @discord.ui.button(label="Next", custom_id="next_elden_ring", style=discord.ButtonStyle.primary, row=4)
    async def next_callback(self, button, interaction):
        current_user = str(interaction.user)
        end_conditions = helper.check_end_early(self.__choices_made, current_user, self.players, self.__players_ready)
        # checking if all choices were made
        if end_conditions[0]:
            await interaction.response.send_message("Please select a choice from each section and try again",
                                                    delete_after=5)
            return

        if end_conditions[1]:
            await interaction.response.send_message(f"Player {current_user} has readied;"
                                                    f" {len(self.__players_ready)} players ready.",
                                                    delete_after=5)
            return

        # needs to be nested loops when implementing choices other than bosses, will do later
        important = ""
        if self.__important_only == "Yes":
            important = " important: true,"
        for goal in self.goal_choices:
            for difficulty in self.difficulty_choice:
                query_request = f"""
                        query {{
                            {goal}(difficulty: "{str(difficulty)}",{important}  limit: 50) {{
                                name
                                region
                                location
                                image
                            }}
                        }}
                        """
                # getting response
                api_response = requests.post(url=QUERY_URL, json={"query": query_request})
                if api_response.status_code == 200:  # will be 200 if api request was successful
                    responses_list = json.loads(api_response.text[16:-3])
                    self.goal_list += responses_list

        # sorting goal_list and randomizing within difficulty groups
        self.print_list()
        # ending view
        self.clear_items()
        await interaction.response.edit_message(content=f"| Elden Ring Settings:\n"
                                                        f"  Goal = {self.goal_choices}"
                                                        f"  Important Goals = {self.__important_only}",
                                                        view=self)
        self.stop()

    def print_list(self):
        for element in self.goal_list:
            print(element)
