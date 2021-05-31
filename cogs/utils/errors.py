import discord
from discord.ext import commands

from cogs.utils.config import get_settings
from cogs.utils.utils import send_basic
from cogs.utils.values import Errors


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

        # Now for the actual error handling
        if isinstance(error, commands.errors.CommandNotFound):
            await send_basic(ctx, **Errors.COMMAND_NOT_FOUND)
        elif isinstance(error, discord.Forbidden):
            await send_basic(ctx, **Errors.FORBIDDEN)
        elif isinstance(error, UserNotRegistered):
            await send_basic(ctx, **Errors.NOT_REGISTERED)
        else:
            await send_basic(ctx, **Errors.OTHER)
        raise error


class UserNotRegistered(commands.CheckFailure):
    """Unregistered user tried running a registered-only command.

    Attributes:
        user: The user that invoked the command
        command: The invoked command
    """

    def __init__(self, user, command):
        self.user = user
        self.command = command

    def __str__(self):
        return 'User "{user}" tried using command "{command}"!'.format(user=self.user, command=self.command)


def is_registered():
    """A :func:`.check` that indicates this command must only be used by registered UniFy users.

    This check raises a special exception, :exc:`.UserNotRegistered`
    that is inherited from :exc:`.CheckFailure`.
    """

    def predicate(ctx):
        verified = get_settings('users.json', 'verified')
        if str(ctx.author.id) not in verified.keys():
            raise UserNotRegistered(ctx.author, ctx.command)
        return True

    return commands.check(predicate)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
