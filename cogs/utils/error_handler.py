
'''
import discord
from discord.ext import commands

from cogs.utils.discord_values import DEFAULT_COLOR


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
        if cog and cog.has_error_handler():
            return

        # Grab our error
        error = getattr(error, 'original', error)

        ignored = ()  # Add ignored errors here!
        if isinstance(error, ignored):
            return

        e = discord.Embed(color=DEFAULT_COLOR)
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


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
'''
