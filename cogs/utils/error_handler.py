import time
import discord
from discord.ext import commands

from cogs.utils import values


def log(message):
    print('\n', time.asctime(time.localtime()), ':', message)


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        :param ctx: The context invoking the command
        :param error: The Exception raised
        """
        # If I'm getting an error from an error handler, ignore it
        if hasattr(ctx.command, 'on_error'):
            return
        # Make sure we're not overriding an error handler, if the cog has it
        cog = ctx.cog
        if cog is not None and cog.has_error_handler():
            return

        # Grab our error
        error = getattr(error, 'original', error)

        ignored = ()  # Add ignored errors here!
        if isinstance(error, ignored):
            return

        e = discord.Embed(color=values.DEFAULT_COLOR)
        if isinstance(error, commands.errors.CommandNotFound):
            e.add_field(name='Command not found!',
                        value='Please check the spelling and try again.')
        elif isinstance(error, discord.Forbidden):
            e.add_field(name='DM could not be sent!',
                        value='Please temporarily allow Direct Messages from other server members '
                              'to continue with the registration process.')
        elif isinstance(error, discord.HTTPException):
            e.add_field(name='I tried giving you the Verified role, but something went wrong!',
                        value='If you are experiencing issues, please contact us using "!mail {message}".')
        else:
            e.add_field(name='There was an error!',
                        value='We don\'t know exactly what happened there. Please try again.')
        await ctx.send(embed=e)
        raise error


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
