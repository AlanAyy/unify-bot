import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, group
from cogs.utils.config import *


# https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html
# https://stackoverflow.com/questions/50548316/subcommands-in-python-bot
# https://stackoverflow.com/questions/52593777/permission-check-discord-py-bot


async def make_group(ctx, name, category=None):
    # Gotta make a role and channel for each
    # Make role
    role = await ctx.guild.create_role(name=name)
    permissions = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
        role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    # Make channel with permissions
    await ctx.guild.create_text_channel(name, overwrites=permissions, category=category)
    # Make voice chat with permissions
    await ctx.guild.create_voice_channel(name, overwrites=permissions, category=category)
    # Use the following if the permissions dict isn't working
    #   channel.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
    #   channel.set_permissions(role, read_messages=True, send_messages=True)


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @group(pass_context=True)  # Setting up `!group` subcommands with @group
    async def groups(self, ctx):
        """Makes new groups (role and channel) for each semester"""
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(color=discord.Colour.orange())
            embed.add_field(name='Command not found!',
                            value='!group new [name] [#] (Make sure [name] includes a "?" if making 2+ groups)\n' +
                                  '!group set [name] (Add yourself to a group)')
            return await ctx.send(embed=embed)

    @groups.command(pass_context=True)
    @has_permissions(administrator=True)  # Checks if the user's an admin
    async def new(self, ctx, name, num: int = None):
        # Default wildcard character is '?'
        wildcard = get_settings('config', 'wildcard')
        # If you have 'saturdays-? {num}', it will check {num} to make that many groups and roles
        # Otherwise it will just make one channel
        embed = discord.Embed(color=discord.Colour.orange())

        if num is None:
            embed.add_field(name='Group successfully created!', value=name)
            await ctx.send(embed)
            return await make_group(ctx, name)
        elif wildcard in name:
            category_name = name.replace('-', '').replace(wildcard, '')
            category = await ctx.guild.create_category(category_name)
            group_names = []
            # Makes {i} channels and roles, replacing {wildcard} with {i}
            for i in range(num):
                iter_name = name.replace(wildcard, str(i + 1))
                group_names.append(iter_name)
                await make_group(ctx, iter_name, category)
            # Add to group list
            write_settings('groups', 'groups', group_names)
            embed.add_field(name='Groups successfully created!',
                            value='{first}\n...\n{last}'.format(first=name.replace(wildcard, '1'),
                                                                last=name.replace(wildcard, str(num))))
            return await ctx.send(embed=embed)

        embed.add_field(name='Group creation failed!',
                        value='Missing wildcard character [{wildcard}]'.format(wildcard=wildcard))
        return await ctx.send(embed=embed)

    @groups.command(pass_context=True)
    async def set(self, ctx, group_name):
        embed = discord.Embed(color=discord.Colour.orange())
        for channel in ctx.guild.channels:
            # TODO: Make whitelist
            if (group_name == channel.name and
                    group_name.lower() not in ['exec', 'president', 'mentor', 'lecture lead', 'jr exec']):
                # It will attempt to give them the role with the same channel name
                embed.add_field(name='Role added!', value=group_name)
                await ctx.send(embed=embed)
                return await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name=group_name))
        embed.add_field(name='Role could not be added!', value=group_name)
        return await ctx.send(embed=embed)

    @groups.command(pass_context=True)
    async def delete(self, ctx, *args):
        # TODO: Make "delete" command
        # TODO: Confirm channel deletion
        embed = discord.Embed(color=discord.Colour.orange())
        embed.add_field(name='Command is under construction...', value='')
        return await ctx.send(embed=embed)

    @groups.command(pass_context=True)
    async def clear(self, ctx, *args):
        # TODO: Make "clear" command
        # TODO: Confirm channel clearing
        embed = discord.Embed(color=discord.Colour.orange())
        embed.add_field(name='Command is under construction...', value='')
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))
