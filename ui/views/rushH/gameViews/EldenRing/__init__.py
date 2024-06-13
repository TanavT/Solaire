import discord
from ui.views.BaseView import BaseView

NUMBER_OF_REGIONS = 10


class EldenRing(BaseView):
    def __init__(self, message: str):
        super().__init__(message)

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
        await interaction.response.defer()

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
        await interaction.response.defer()

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
        await interaction.response.defer()

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary, row=3)
    async def next_callback(self, button, interaction):
        # pulls from elden_ring database, elden ring api needs to be running during this
        query_url = "http://localhost:3000/api/graphql"  # assumes the api is running on this computer
        query_body = """ 
                query {
                    boss(region: "Limgrave",  limit: 50) {
                        name
                        location
                        image
                        difficulty
                    }
                }
                """
        await interaction.response.defer()
