# NOTE: This file is solely for testing new features in a contained space, none of the utilities defined in this file
# are meant to be used in the normal operation of the bot

import discord
from discord.ext import commands
import requests
import json
from discord.ext.pages import Paginator, Page
import discord.ui.view
from ui.views.rushH.PlayerJoin import PlayerJoin
import time

embed_test = discord.Embed(
            title="My Amazing Embed",
            description="Embeds are super easy, barely an inconvenience.",
            color=discord.Colour.blurple(),  # Pycord provides a class with default colors you can choose from
        )


class PlayerJoinView(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.num = 0
        self.timer_started = False
        self.start_time = 0
        self.times_button_pressed = 0

    @discord.ui.button(label="Slot 1", style=discord.ButtonStyle.secondary, row=0)
    async def slot1_callback(self, button, interaction):
        if button.style != discord.ButtonStyle.success:
            button.style = discord.ButtonStyle.success
            button.label = str(interaction.user)
        else:
            button.style = discord.ButtonStyle.secondary
            button.label = "Slot 1"
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 2", style=discord.ButtonStyle.secondary, row=0)
    async def slot2_callback(self, button, interaction):
        if button.style != discord.ButtonStyle.success:
            button.style = discord.ButtonStyle.success
            button.label = str(interaction.user)
        else:
            button.style = discord.ButtonStyle.secondary
            button.label = "Slot 2"
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 3", style=discord.ButtonStyle.secondary, row=0)
    async def slot3_callback(self, button, interaction):
        if button.style != discord.ButtonStyle.success:
            button.style = discord.ButtonStyle.success
            button.label = str(interaction.user)
        else:
            button.style = discord.ButtonStyle.secondary
            button.label = "Slot 3"
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Slot 4", style=discord.ButtonStyle.secondary, row=0)
    async def slot4_callback(self, button, interaction):
        if button.style != discord.ButtonStyle.success:
            button.style = discord.ButtonStyle.success
            button.label = str(interaction.user)
        else:
            button.style = discord.ButtonStyle.secondary
            button.label = "Slot 4"
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Start Game", style=discord.ButtonStyle.primary, row=1)
    async def start_game_callback(self, button, interaction):
        # self.disable_all_items()
        await interaction.user.send(content='Greetings!', embed=embed_test, view=PlayerButtonView(self))
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Check Times Pressed", style=discord.ButtonStyle.primary, row=1)
    async def check_presses_callback(self, button, interaction):
        await interaction.response.send_message(f"Time Button Pressed: {self.times_button_pressed}")

    @discord.ui.button(label="Start Timer", style=discord.ButtonStyle.primary, row=4)
    async def start_timer_callback(self, button, interaction):
        timer_length = 3
        if not self.timer_started:
            self.start_time = time.time()
            self.timer_started = True

        current_time = time.time()
        if current_time - self.start_time >= timer_length:
            self.disable_all_items()
            await interaction.response.send_message("Timer Elapsed")
            button.label = "Time Remaining : 00:00"
            self.stop()
        else:
            button.label = f"Time Remaining: {convert_seconds_to_clock(timer_length - (current_time - self.start_time))}"
            await interaction.response.edit_message(view=self)


class PlayerButtonView(discord.ui.View):

    def __init__(self, parent_view: PlayerJoinView):
        super().__init__()
        self.__parent_view = parent_view

    @discord.ui.button(label="Press Me", style=discord.ButtonStyle.secondary, row=0)
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("Button Pressed")
        self.__parent_view.times_button_pressed += 1


# need to get a better database, problem is that there is no others I can find
# This database is not consistent with locations and regions, I will try to fix later ig
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


class TestingSpaceClass(commands.Cog):

    @discord.slash_command()
    async def greetings(self, ctx):
        await ctx.respond('Greetings!')

    @discord.user_command()
    async def person_greeting(self, ctx, member: discord.Member):
        await ctx.respond(f'{ctx.author.mention} says hello to {member.mention}')

    @discord.slash_command()
    async def player_slots(self, ctx):
        await ctx.respond("Waiting for Players...", view=PlayerJoinView())

    @discord.slash_command()
    async def api_pull(self, ctx):
        url = "http://localhost:3000/api/graphql"
        body = """ 
        query {
            boss(region: "Limgrave",  limit: 50) {
                name
                location
                image
                difficulty
            }
        }
        """

        # need to get a better database, problem is that there is no others I can find
        # This database is not consistent with locations and regions, I will try to fix later ig

        response = requests.post(url=url, json={"query": body})
        print("response status code: ", response.status_code)
        if response.status_code == 200:  # checking if successfully received
            # print(response.text[16:-3])
            responses_list = json.loads(response.text[16:-3])
            # print("response : ", response)
            for index in range(len(responses_list)):
                # print("name: ", responses_list[index]["name"], ", region", responses_list[index]["region"], ", location: ", responses_list[index]["location"], ", image: ", responses_list[index]["image"],)
                print(responses_list[index])
        await ctx.respond("api pulled")

    @discord.slash_command()
    async def changing_pages(self, ctx):
        embed = discord.Embed(
            title="My Amazing Embed",
            description="Embeds are super easy, barely an inconvenience.",
            color=discord.Colour.blurple(),  # Pycord provides a class with default colors you can choose from
        )
        embed.add_field(name="A Normal Field",
                        value="A really nice field with some information. **The description as well as the fields support markdown!**")

        embed.add_field(name="Inline Field 1", value="Inline Field 1", inline=True)
        embed.add_field(name="Inline Field 2", value="Inline Field 2", inline=True)
        embed.add_field(name="Inline Field 3", value="Inline Field 3", inline=True)

        embed.set_footer(text="Footer! No markdown here.")  # footers can have icons too
        embed.set_author(name="Pycord Team", icon_url="https://example.com/link-to-my-image.png")
        embed.set_thumbnail(url="https://example.com/link-to-my-thumbnail.png")
        embed.set_image(url="https://eldenring.wiki.fextralife.com/file/Elden-Ring/"
                            "elden_ring_artwork_elden_ring_wiki_guide_7_300px.jpg")

        await ctx.respond("Hello! Here's a cool embed.", embed=embed, view=PlayerJoin("| Waiting for Players...", []))  # Send the embed with some text

# class TestingEmbedView(discord.ui.View):
#     def __init__(self, ctx):
#         super().__init__()
#         self.num = 0
#
#     async def send(self,ctx):
#         self.message = await ctx.send(view=self)
#         await self.update_message()
#
#     def create_embed(self):
#         embed = discord.Embed(title=f"User List Page {self.num}")
#         return embed
#     async def update_message(self,ctx):
#         await self.message.edit(embed=self.create_embed(), view=self)
#
#     @discord.ui.button(label="Incrementor", style=discord.ButtonStyle.secondary, row=0)
#     async def embed_test(self, button: discord.ui.Button, interaction: discord.Interaction):
#         await interaction.response.defer()
    @discord.slash_command()
    async def greetings_private(self, ctx):
        await ctx.author.send('Greetings!')

    @discord.slash_command()
    async def timer(self, ctx):
        start_time = time.time()
        current_time = time.time()
        while current_time - start_time < 3:
            current_time = time.time()
            await ctx.respond(f'Time: {current_time - start_time}')


def setup(bot):
    bot.add_cog(TestingSpaceClass(bot))
