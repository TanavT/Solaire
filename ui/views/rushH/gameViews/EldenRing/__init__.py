import discord
from ui.views.BaseView import BaseView
import json
import requests
import cogs.helper.rushH.helper_funcs as helper

NUMBER_OF_REGIONS = 10
NUM_CHOICES = 3


# will return
class EldenRing(BaseView):
    def __init__(self, message: str, player: list):
        super().__init__(message, player)
        self.__players_ready = []
        self.__region_choices = None
        self.selection_choice = None
        self.__goal_choices = None
        self.goal_list = []
        self.__choices_made = NUM_CHOICES * [False]

    @discord.ui.select(
        placeholder="Regions (Nothing Selected)",
        min_values=1,
        max_values=NUMBER_OF_REGIONS,
        row=0,
        options=[
            discord.SelectOption(
                label="Limgrave"
            ),
            discord.SelectOption(
                label="Weeping Peninsula"
            ),
            discord.SelectOption(
                label="Liurnia of the Lakes"
            ),
            discord.SelectOption(
                label="Siofra River"
            ),
            discord.SelectOption(
                label="Ainsel River"
            ),
            discord.SelectOption(
                label="Caelid"
            ),
            discord.SelectOption(
                label="Altus Plateau"
            ),
            discord.SelectOption(
                label="Nokron, Eternal City"
            ),
            discord.SelectOption(
                label="Deeproot Depths"
            ),
            discord.SelectOption(
                label="Capital Outskirts"
            ),
            discord.SelectOption(
                label="Mount Gelmir"
            ),
            discord.SelectOption(
                label="Lake of Rot"
            ),
            discord.SelectOption(
                label="Dragonbarrow"
            ),
            discord.SelectOption(
                label="Leyndell, Royal Capital"
            ),
            discord.SelectOption(
                label="Moonlight Altar"
            ),
            discord.SelectOption(
                label="Mountaintops of the Giants"
            ),
            discord.SelectOption(
                label="Consecrated Snowfield"
            ),
            discord.SelectOption(
                label="Mohgwyn Palace"
            ),
            discord.SelectOption(
                label="Miquella's Haligtree"
            ),
            discord.SelectOption(
                label="Leyndell, Ashen Capital"
            ),
        ]
    )
    async def region_choice_callback(self, select, interaction):
        self.__choices_made[0] = True
        self.__region_choices = []
        for region in select.values:
            self.__region_choices += [region]
        await interaction.response.send_message(f"Player '{str(interaction.user)}' chose region: "
                                                f"'{self.__region_choices}'",
                                                delete_after=3)

    @discord.ui.select(
        placeholder="Selection Pattern (Nothing Selected)",
        min_values=1,
        max_values=1,
        row=1,
        options=[
            discord.SelectOption(
                label="Progressive",
                description="Earlier/Easier Content at the beginning, Later/Harder content at the end"
            ),
            discord.SelectOption(
                label="Random",
                description="Pseudo-random (look it up) selection"
            )
        ]
    )
    async def selection_choice_callback(self, select, interaction):
        self.__choices_made[1] = True
        self.selection_choice = select.values[0]
        await interaction.response.send_message(f"Player '{str(interaction.user)}' chose pattern: "
                                                f"'{self.selection_choice}'",
                                                delete_after=3)

    @discord.ui.select(
        placeholder="Goal (Nothing Selected)",
        min_values=1,
        max_values=3,
        row=2,
        options=[
            discord.SelectOption(
                label="Bosses",
            ),
            discord.SelectOption(
                label="Weapons",
            ),
            discord.SelectOption(
                label="Spells/Incantations/AoW",
            )
        ]
    )
    async def goal_choice_callback(self, select, interaction):
        self.__choices_made[2] = True
        self.__goal_choices = []
        for goal in select.values:
            self.__goal_choices += [goal]
        await interaction.response.send_message(f"Player '{str(interaction.user)}' chose goals: "
                                                f"'{self.__goal_choices}'",
                                                delete_after=3)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary, row=3)
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

        # pulls from elden_ring database, elden ring api needs to be running during this
        query_url = "http://localhost:3000/api/graphql"  # assumes the api is running on this computer

        # needs to be nested loops when implementing choices other than bosses, will do later
        for region in self.__region_choices:
            query_request = f"""
                    query {{
                        boss(region: "{region}",  limit: 50) {{
                            name
                            location
                            image
                            difficulty
                        }}
                    }}
                    """
            # getting response
            api_response = requests.post(url=query_url, json={"query": query_request})
            # print(self.__region_choices)
            # print("response status code: ", api_response.status_code)  # for debugging purpose, will print in terminal
            if api_response.status_code == 200:  # will be 200 if api request was successful
                responses_list = json.loads(api_response.text[16:-3])
                #  index in range(len(responses_list)):
                #    self.__goal_choices += [responses_list[index]]
                #    print(responses_list[index])
                self.goal_list += responses_list

        # print(self.goal_list)
        for index in range(len(self.goal_list)):
            print(self.goal_list[index])

        # ending view
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        self.stop()
