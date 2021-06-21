import re

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

        # General errors
        if isinstance(error, commands.errors.CommandNotFound):
            await send_basic(ctx, **Errors.COMMAND_NOT_FOUND)
        elif isinstance(error, commands.MissingRequiredArgument):
            await send_basic(ctx, **Errors.MISSING_ARGUMENT)
        elif isinstance(error, InvalidArgument):
            await send_basic(ctx, **Errors.INVALID_ARGUMENT)
        elif isinstance(error, discord.Forbidden):
            await send_basic(ctx, **Errors.FORBIDDEN)
        elif isinstance(error, UserNotRegistered):
            await send_basic(ctx, **Errors.NOT_REGISTERED)
        # Command-specific errors
        elif isinstance(error, commands.PrivateMessageOnly):
            await send_basic(ctx, **Errors.DM_ONLY)
        elif isinstance(error, commands.NoPrivateMessage):
            await send_basic(ctx, **Errors.GUILD_ONLY)
        elif isinstance(error, ExpiredEmailToken):
            await send_basic(ctx, **Errors.EXPIRED_TOKEN)
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
        return 'Unregistered user "{user}" tried using command "{cmd}"!'.format(user=self.user, cmd=self.command)


class InvalidArgAmount(commands.CommandError):

    def __init__(self, user, command, args_len):
        self.user = user
        self.command = command
        self.args_len = args_len

    def __str__(self):
        return '"{user}" tried running command "{cmd}" with {args_len} args!' \
            .format(user=self.user, cmd=self.command, args_len=self.args_len)


class InvalidArgument(commands.CommandError):

    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return '"{arg}" is not a valid argument!'.format(arg=self.arg)


class ExpiredEmailToken(commands.CommandError):

    def __init__(self):
        pass

    def __str__(self):
        return 'Email token is expired! Please acquire a new token.'


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


def is_valid_arg(arg: str, arg_type: str):
    if arg_type == 'id' and (re.search('[a-zA-Z]', arg) is not None or len(arg) != 18):
        raise InvalidArgument('id')
    elif arg_type == 'invite' and 'https://discord.gg/' not in arg:
        raise InvalidArgument('invite')
    return True


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
