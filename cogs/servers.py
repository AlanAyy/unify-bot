import discord
from discord.ext import commands
from discord.ext.commands import group, has_permissions

from cogs.utils.embeds import DEFAULT_COLOUR


class Servers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    ###########################
    #                         #
    #   ADMIN-ONLY COMMANDS   #
    #                         #
    ###########################

    @group()
    async def servers(self, ctx):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(color=DEFAULT_COLOUR)
            e.add_field(name='Invalid subcommand!',
                        value='Please type "!help servers" to get started!')
            return await ctx.send(e)

    @servers.command(description='Request to have a server added to the database. A verified role must exist.',
                     usage='{server ID} {name} {permanent invite} {ID of "verified role"}')
    @has_permissions(administrator=True)
    async def add(self, ctx, *args):
        # TODO: Send a DM to Owner requesting to add a server to the database
        server, name, link, verified_role = args
        e = discord.Embed(color=DEFAULT_COLOUR)

        return await ctx.send(embed=e)
        pass

    @servers.command(description='',
                     usage='')
    @has_permissions(administrator=True)
    async def blacklist(self, ctx):
        # TODO: Send a DM to Owner requesting to add a user to the blacklist with a reason
        e = discord.Embed(color=DEFAULT_COLOUR)

        return await ctx.send(embed=e)
        pass

    #####################
    #                   #
    #   USER COMMANDS   #
    #                   #
    #####################

    @servers.command(description='',
                     usage='')
    async def list(self, ctx):
        # TODO: DM a list of all relevant servers from the same domain
        e = discord.Embed(color=DEFAULT_COLOUR)

        return await ctx.send(embed=e)
        pass

    @commands.command()
    async def invite(self, ctx):
        default_url = 'https://discord.com/api/oauth2/authorize' \
                      '?client_id=843981504785809438' \
                      '&permissions={perms}' \
                      '&scope=bot'
        msg_perms = default_url.format(perms='2048')
        role_perms = default_url.format(perms='268437504')
        e = discord.Embed(color=DEFAULT_COLOUR)
        e.add_field(name='Invite UniFy to your server!',
                    value='[Send Messages only]({url})'.format(url=msg_perms) +
                          '\n[Manage Roles + Send Messages]({url})'.format(url=role_perms))

        return await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Servers(bot))
