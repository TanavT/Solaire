import discord
from discord.ext import commands
import random

class diceRoll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @discord.slash_command()
    async def dice_roll(self, ctx, num_of_dice: int, dice_sides: int):
        if dice_sides <= 0:
            # raise commands.BadArgument("dice_sides must be greater than or equal to 0.")
            await ctx.respond("dice_sides must be greater than or equal to 0.", ephemeral=True)
            return False
        if num_of_dice <= 0:
            # raise commands.BadArgument("num_of_dice must be greater than or equal to 0.")
            await ctx.respond("num_of_dice must be greater than or equal to 0.", ephemeral=True)
            return False

        rolls = []
        total = 0
        for i in range(num_of_dice):
            dice_roll = random.randint(1, dice_sides)
            rolls += [dice_roll]
            total += dice_roll
        embed = discord.Embed(
            title=f"Rolling Dice",
            description=f"Rolling {num_of_dice}d{dice_sides}",
            color=discord.Color.red()
        )
        embed.add_field(name=f"Rolls", value=f"{rolls}", inline=False)
        embed.add_field(name=f"Total", value=f"{total}", inline=False)

        embed.set_footer(text=f"Generic Dice Roller")
        embed.set_author(name="Solaire of Astora")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(diceRoll(bot))
