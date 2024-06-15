import discord
from ui.views.BaseView import BaseView
import json
import requests
import cogs.helper.rushH.helper_funcs as helper

NUMBER_OF_REGIONS = 10
NUM_CHOICES = 3
# pulls from elden_ring database, elden ring api needs to be running during this
QUERY_URL = "http://localhost:3000/api/graphql"


# output is list of goals found in goal_list, contains name, image, region, location, and difficulty
class EldenRing(BaseView):
    def __init__(self, message: str, player: list):
        super().__init__(message, player)
        self.__players_ready = []
        self.__region_choices = None
        self.pattern_choice = None
        self.__goal_choices = None
        self.goal_list = []
        self.__choices_made = NUM_CHOICES * [False]
        self.color = discord.Color.dark_gold()

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
                label="Crumbling Farum Azula"
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
        placeholder="Goal Pattern (Nothing Selected)",
        min_values=1,
        max_values=1,
        row=1,
        options=[
            discord.SelectOption(
                label="Progressive Choice",
                description="Earlier/Easier Content at the beginning, Later/Harder content at the end"
            ),
            discord.SelectOption(
                label="Random Choice",
                description="Pseudo-random (look it up) selection"
            ),
            discord.SelectOption(
                label="Progressive Choice& Ramping",
                description="Earlier/Easier Content at the beginning, Later/Harder content at the end"
            ),
            discord.SelectOption(
                label="Random ",
                description="Pseudo-random (look it up) selection"
            )
        ]
    )
    async def pattern_choice_callback(self, select, interaction):
        self.__choices_made[1] = True
        self.pattern_choice = select.values[0]
        await interaction.response.send_message(f"Player '{str(interaction.user)}' chose pattern: "
                                                f"'{self.pattern_choice}'",
                                                delete_after=3)

    @discord.ui.select(
        placeholder="Goal (Nothing Selected)",
        min_values=1,
        max_values=3,
        row=2,
        options=[
            discord.SelectOption(
                label="Boss",
            ),
            discord.SelectOption(
                label="Weapon",
            ),
            discord.SelectOption(
                label="Spell/Incantation/AoW",
            )
        ]
    )
    async def goal_choice_callback(self, select, interaction):
        self.__choices_made[2] = True
        self.__goal_choices = []
        for goal in select.values:
            self.__goal_choices += [goal.lower()]
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

        # needs to be nested loops when implementing choices other than bosses, will do later
        for goal in self.__goal_choices:
            for region in self.__region_choices:
                query_request = f"""
                        query {{
                            {goal}(region: "{region}",  limit: 50) {{
                                name
                                region
                                location
                                image
                                difficulty
                            }}
                        }}
                        """
                # getting response
                api_response = requests.post(url=QUERY_URL, json={"query": query_request})
                if api_response.status_code == 200:  # will be 200 if api request was successful
                    responses_list = json.loads(api_response.text[16:-3])
                    self.goal_list += responses_list

            # print(self.goal_list)
            # for index in range(len(self.goal_list)):
            #     print(self.goal_list[index])

            # ending view
            self.disable_all_items()
            await interaction.response.edit_message(view=self)
            self.stop()
