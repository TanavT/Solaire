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
                label="Caelid"
            ),
            discord.SelectOption(
                label="Mt. Gelmir"
            ),
            discord.SelectOption(
                label="Altus Plateau"
            ),
            discord.SelectOption(
                label="Leyndell, Royal Capital"
            ),
            discord.SelectOption(
                label="Mountaintop of the Giants"
            ),
            discord.SelectOption(
                label="Consecrated Snowfield"
            ),
            discord.SelectOption(
                label="Haligtree"
            )
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
        await interaction.response.defer()
