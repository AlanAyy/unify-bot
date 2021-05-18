import discord
from discord import Member
from discord.ext.commands import Context

from cogs.utils.discord_values import DEFAULT_COLOR


# def mail(bot: Bot, ctx: Context, message: str, confirmation=True):
#     """Send mail to the owner"""
#     # Get owner ID
#     owner_id = get_settings('config.json', 'owner_id')
#     me = await bot.fetch_user(owner_id)
#
#     # Messaging time
#     e = discord.Embed(color=discord.Colour.orange(), description=ctx.author.mention)
#     e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
#     e.add_field(name='Mail', value=message)
#
#     await me.send(embed=e)
#
#     e = discord.Embed(title='Message sent!', color=discord.Colour.orange(), description=ctx.author.mention)
#     return await ctx.send(embed=e)


async def dm(user: Member, ctx: Context, message: str, confirmation_msg: str = None, display_author=True,
             title=None, color=DEFAULT_COLOR, description=None, name='DM'):
    """
    :param user: A Member object of the user who will receive the DM
    :param ctx: The context of the request to DM
    :param message: The message to be sent
    :param confirmation_msg: Should there be a confirmation message? If so, what should it say?
    :param display_author: Whether the author should be displayed in the DM
    :param title: Embed title
    :param color: Embed color
    :param description: Embed description (defaults to ctx.author.mention)
    :param name: Name of the message (defaults to 'DM')
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

    return await user.send(embed=e)
