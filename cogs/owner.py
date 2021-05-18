from discord.ext import commands


# https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html
# https://stackoverflow.com/questions/50548316/subcommands-in-python-bot
# https://stackoverflow.com/questions/52593777/permission-check-discord-py-bot


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Owner(bot))
