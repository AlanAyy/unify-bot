import discord
from discord import Member
from discord.ext.commands import Context

from cogs.utils.config import get_settings
from cogs.utils.values import DEFAULT_COLOR
from cogs.utils.error_handler import log


async def dm(user: Member, ctx: Context, message: str, confirmation_msg: str = None, display_author=True,
             title=None, color=DEFAULT_COLOR, description=None, name='Direct Message!'):
    """
    Send a direct message to a user
    :param user: A Member object of the user who will receive the DM
    :param ctx: The Context of the request to DM
    :param message: The message to be sent
    :param confirmation_msg: Should there be a confirmation message? If so, what should it say?
    :param display_author: Whether the author should be displayed in the DM
    :param title: Embed title
    :param color: Embed color
    :param description: Embed description (defaults to ctx.author.mention)
    :param name: Name of the message (defaults to 'Direct Message!')
    :return: Returns the DM sent
    """
    embed_description = (ctx.author.mention if description is None else description)

    e = discord.Embed(title=title, color=color, description=embed_description)
    if display_author:
        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    e.add_field(name=name, value=message)

    if confirmation_msg is not None:
        e2 = discord.Embed(title=confirmation_msg, color=DEFAULT_COLOR, description=ctx.author.mention)
        await ctx.send(embed=e2)

    log('Sent a DM to {.name}!'.format(user))
    return await user.send(embed=e)


async def send_basic(ctx: Context, title: str = None, name: str = None, value: str = None,
                     description=None, display_author=True, color=DEFAULT_COLOR):
    """
    Send a basic message with one text field
    :param ctx: The Context of the command call
    :param title: Embed title
    :param name: Name of the text field
    :param value: Value of the text field
    :param description: Embed description (defaults to ctx.author.mention)
    :param display_author: Whether the author should be displayed in the DM
    :param color: Embed color
    :return: Returns the message sent
    """
    embed_description = (ctx.author.mention if description is None else description)

    e = discord.Embed(title=title, color=color, description=embed_description)
    if display_author:
        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    if name is not None and value is not None:
        e.add_field(name=name, value=value)

    return await ctx.send(embed=e)


def is_registered(user: Member) -> bool:
    """
    Checks if a user is registered with UniFy
    :param user: The User to check
    :return: Returns True if they're registered, False otherwise
    """
    verified = get_settings('users.json', 'verified')
    if str(user.id) in verified.keys():
        return True
    return False
