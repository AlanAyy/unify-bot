import re

import discord
from discord.ext import commands
from discord.ext.commands import group, has_permissions

from cogs.utils import user_util
from cogs.utils.config import get_settings, write_settings
from cogs.utils.discord_values import DEFAULT_COLOR
from cogs.utils.logger import log


class Servers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._use_help = 'Please use "!help servers request" for more information.'

    ###########################
    #                         #
    #   ADMIN-ONLY COMMANDS   #
    #                         #
    ###########################

    @group(aliases=['server'])
    async def servers(self, ctx):
        if ctx.invoked_subcommand is None:
            e = discord.Embed(color=DEFAULT_COLOR)
            e.add_field(name='Invalid subcommand!',
                        value='Please type "!help servers" to get started!')
            return await ctx.send(e)

    @servers.command(description='Request to have a server added to the database. A verified role must exist.'
                                 '\n\nTo get your server ID, right-click your server icon and select "Copy ID".'
                                 '\nTo get a permanent invite, click on your server name and select "Invite '
                                 'People". Next, select "Edit invite link", select "EXPIRE AFTER: Never" '
                                 'and "MAX NUMBER OF USES: No Limit", then "Generate a New Link", then "Copy".'
                                 '\nTo get your verified role ID, click on your server name and navigate to '
                                 'Server Settings > Roles. If you do not have a Verified role, create one. '
                                 'If you do, hover over it, select "More", then "Copy ID".',
                     usage='{server ID} {"name in quotation marks"} {permanent invite} {Verified role ID}')
    @has_permissions(administrator=True)
    @commands.cooldown(1, 30.0, commands.BucketType.user)  # Once every 30s per user
    async def request(self, ctx, *, message):
        # TODO: Proper error handling on cases with incorrect amount of args (should be 4)
        e = discord.Embed(color=DEFAULT_COLOR)

        # Check if user is registered with UniFy first
        if not user_util.is_registered(ctx.author):
            e.add_field(name='You are not registered!',
                        value='Please complete your registration using "!register" before running this command.')

        # Get bot owner info
        owner_id = get_settings('config.json', 'owner_id')
        me = await self.bot.fetch_user(owner_id)

        # Error handling time
        try:
            # Fancy regex voodoo to parse user args c:
            args = re.compile('["\']\\s+|\\s+["\']').split(message)
            args[2:] = re.compile('\\s+').split(args[2])
        except IndexError as error:
            e.add_field(name='Invalid use of command!',
                        value=self._use_help)
            await ctx.send(embed=e)
            raise error

        # More error handling time
        server_id, name, invite, verified_role = args
        # If there's a letter in the Server ID, or if it's not 18 numbers long
        if re.search('[a-zA-Z]', server_id) is not None or len(server_id) != 18:
            error_message = 'Invalid server ID!'
        # If the invite link is not a link
        elif 'https://discord.gg/' not in invite:
            error_message = 'Invalid invite link!'
        # Same checks as Server ID but on the Role ID instead
        elif re.search('[a-zA-Z]', verified_role) is not None or len(verified_role) != 18:
            error_message = 'Invalid Verified role ID!'
        # If it's all valid
        else:
            await user_util.dm(me, ctx,
                               '''
                               Server ID: {0}
                               Name: {1}
                               Invite Link: {2}
                               Verified Role ID: {3}'''.format(*args),
                               confirmation_msg='Request sent successfully!',
                               name='Server request!', )
            return  # Make sure we're not sending two messages
        e.add_field(name=error_message, value=self._use_help)
        return await ctx.send(embed=e)

    @servers.command(description='Add a server to the database.',
                     usage='{domain} {"category"} {server ID} {"name"} {permanent invite} {ID of "verified role"}')
    @commands.is_owner()  # Only the bot owner may run this command c:
    @commands.dm_only()
    async def add(self, ctx, *, message):
        # TODO: Auto backup of users.json and servers.json files
        # Same fancy regex voodoo magic
        args = re.compile('["\']\\s+|\\s+["\']').split(message)
        args[4:] = re.compile('\\s+').split(args[4])

        domain, category, server_id, name, invite, verified_role = args
        settings_data = get_settings('servers.json', domain)
        data = {
            category: {
                server_id: {
                    "name": name,
                    "invite": invite,
                    "verified_role": verified_role
                }
            }
        }
        if settings_data['servers'].get(category) is not None:
            data = data[category]
            settings_data['servers'][category].update(data)
            write_settings('servers.json', domain, settings_data, mode='update')
        # If category does not exist
        else:
            settings_data['servers'].update(data)
            write_settings('servers.json', domain, settings_data, mode='update')

        log('Server {name} added to servers.json!'.format(name=name))
        e = discord.Embed(title='Server "{name}" successfully added!'.format(name=name), color=DEFAULT_COLOR)
        e.add_field(name='Domain: {0[0]}'.format(args),
                    value='''Category: {0[1]}
                    Server ID: {0[2]}
                    Name: {0[3]}
                    Invite Link: {0[4]}
                    Verified Role: {0[5]}'''.format(args))

        return await ctx.send(embed=e)

    @servers.command(description='',
                     usage='')
    @has_permissions(administrator=True)
    async def blacklist(self, ctx):
        # TODO: Send a DM to Owner requesting to add a user to the blacklist with a reason
        e = discord.Embed(color=DEFAULT_COLOR)

        return await ctx.send(embed=e)
        pass

    #####################
    #                   #
    #   USER COMMANDS   #
    #                   #
    #####################

    @servers.command(description='',
                     usage='')
    async def list(self, ctx, *, category=None):
        # TODO: Make a "You must be registered!" default embed
        # TODO: Proper. Fucking. Error. Handling.
        # Check if user is registered with UniFy first
        if not user_util.is_registered(ctx.author):
            e = discord.Embed(color=DEFAULT_COLOR)
            e.add_field(name='You are not registered!',
                        value='Please complete your registration using "!register" before running this command, ' 
                              'or contact us using "!mail {message}" if you are having issues.')
            return await ctx.send(embed=e)

        domain = get_settings('users.json', 'verified').get(str(ctx.author.id)).get('domain')
        categories = get_settings('servers.json', domain).get('servers')
        # If they want to see categories (they called "!servers list")
        if category is None:
            # Get the user's domain, then its server categories
            info = '\n'.join(categories.keys())
        # If they want to see servers (they called "!servers list {category}")
        elif categories.get(category) is not None:
            if ctx.channel == ctx.author.dm_channel:
                servers = categories.get(category)
                # Now this is some crazy shit
                info = '\n'.join('__**{name}**__: *{invite}*'.format(**data) for _, data in servers.items())
            # If they called it in a public channel
            else:
                e = discord.Embed(color=DEFAULT_COLOR)
                e.add_field(name='This command cannot be run in a public channel!',
                            value='Please delete your message, and send the bot a direct message with your '
                                  'command instead. This is in place to protect the privacy of our users.')
                return await ctx.send(embed=e)
        # Category does not exist?
        else:
            e = discord.Embed(color=DEFAULT_COLOR)
            e.add_field(name='That category does not exist!',
                        value='Please complete your registration using "!register" before running this command, '
                              'or contact us using "!mail {message}" if you are having issues.')
            return await ctx.send(embed=e)

        return await user_util.dm(ctx.author, ctx, info, name='Server List')

    @commands.command()
    async def invite(self, ctx):
        default_url = 'https://discord.com/api/oauth2/authorize' \
                      '?client_id=843981504785809438' \
                      '&permissions={perms}' \
                      '&scope=bot'
        # TODO: Hex calculator for perms?
        msg_perms = default_url.format(perms='2048')
        role_perms = default_url.format(perms='268437504')
        e = discord.Embed(color=DEFAULT_COLOR)
        e.add_field(name='Invite UniFy to your server!',
                    value='[Send Messages only]({url})'.format(url=msg_perms) +
                          '\n[Manage Roles + Send Messages]({url})'.format(url=role_perms))

        return await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Servers(bot))
