from typing import Final
import os
from dotenv import load_dotenv
import discord

cogsList = ["testingSpace", "rush"]
# loading token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# setting up bot
bot = discord.Bot()


# main entry point
def main() -> None:
    for cog in cogsList:
        bot.load_extension(f'cogs.{cog}')
    bot.run(token=TOKEN)


if __name__ == '__main__':
    main()
