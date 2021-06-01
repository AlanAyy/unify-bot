import re

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

from cogs.utils import errors, utils, values
from cogs.utils.config import get_settings, write_settings
from cogs.utils.utils import log


class Servers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._use_help = 'Please use "!help servers request" for more information.'

    ###########################
    #                         #
    #   ADMIN-ONLY COMMANDS   #
    #                         #
    ###########################

    @commands.group(**values.Commands.SERVERS)
    async def servers(self, ctx):
        # TODO: Might be unnecessary... double-check
        # if ctx.invoked_subcommand is None:
        #     return utils.invalid_subcommand(ctx)
        pass

    @commands.group(**values.Commands.BLACKLIST)
    async def blacklist(self, ctx):
        # TODO: Might be unnecessary... double-check
        # if ctx.invoked_subcommand is None:
        #     return utils.invalid_subcommand(ctx)
        pass

    @servers.command(**values.Commands.SERVERS_REQUEST)
    @commands.dm_only()
    @errors.is_registered()
    @commands.cooldown(1, 30.0, commands.BucketType.user)  # Once every 30s per user
    async def request(self, ctx, *, message):
        # TODO: Proper error handling on cases with incorrect amount of args (should be 4)
        owner = await utils.fetch_owner(self.bot)

        try:
            # Fancy regex voodoo to parse user args c:
            args = re.compile('["\']\\s+|\\s+["\']').split(message)
            args[2:] = re.compile('\\s+').split(args[2])
        except IndexError:
            raise errors.InvalidArguments

        # More error handling time
        server_id, name, invite, verified_role = args
        # If there's a letter in the Server ID, or if it's not 18 numbers long
        if re.search('[a-zA-Z]', server_id) is not None or len(server_id) != 18:
            return await utils.send_basic(ctx, **values.SERVERS_INVALID_SERVER_ID)
        # If the invite link is not a link
        elif 'https://discord.gg/' not in invite:
            return await utils.send_basic(ctx, **values.SERVERS_INVALID_INVITE)
        # Same checks as Server ID but on the Role ID instead
        elif re.search('[a-zA-Z]', verified_role) is not None or len(verified_role) != 18:
            return await utils.send_basic(ctx, **values.SERVERS_INVALID_VERIFIED_ROLE)
        # If it's all valid
        else:
            await utils.dm(owner, ctx,
                           '''
                           Server ID: {0}
                           Name: {1}
                           Invite Link: {2}
                           Verified Role ID: {3}
                           
                           To confirm, use `!servers unify {0} {1} {2} {3}`'''.format(*args),
                           confirmation_msg='Request sent successfully!',
                           name='Server request!')

    @blacklist.command(**values.Commands.BLACKLIST_APPEAL)
    @commands.guild_only()
    @has_permissions(administrator=True)
    @errors.is_registered()
    @commands.cooldown(1, 30.0, commands.BucketType.user)  # Once every 30s per user
    async def appeal(self, ctx, user_id=None, *, reason='No reason provided.'):
        # Check for a valid User ID
        if user_id is None or len(user_id) != 18:
            await utils.send_basic(ctx, **values.SERVERS_INVALID_USER_ID)

        owner = await utils.fetch_owner(self.bot)
        # TODO: Make this "utils.dm" call cleaner?
        await utils.dm(owner, ctx,
                       '''
                       User ID: {user_id}
                       Reason: {reason}
                       
                       To confirm, use `!blacklist ban {user_id}`'''.format(user_id=user_id, reason=reason),
                       confirmation_msg='Appeal sent successfully!',
                       name='BLACKLIST APPEAL!', color=discord.Colour.red())

    #####################
    #                   #
    #   USER COMMANDS   #
    #                   #
    #####################

    @servers.command(**values.Commands.SERVERS_LIST)
    @errors.is_registered()
    async def list(self, ctx, *, category=None):
        domain = get_settings('users.json', 'verified').get(str(ctx.author.id)).get('domain')
        categories = get_settings('servers.json', domain).get('servers')
        # If they want to see categories (they called "!servers list")
        if category is None:
            # Get the user's domain, then its server categories
            info = ('\n'.join(categories.keys()) +
                    '\n\n*Type "!servers list [category]" to continue browsing*')
        # If they want to see servers (they called "!servers list {category}")
        elif categories.get(category) is not None:
            if ctx.channel == ctx.author.dm_channel:
                servers = categories.get(category)
                # Now this is some crazy shit
                info = '\n'.join('__**{name}**__: *{invite}*'.format(**data) for _, data in servers.items())
            # If they called it in a public channel
            else:
                e = discord.Embed(color=values.DEFAULT_COLOR)
                e.add_field(name='This command cannot be run in a public channel!',
                            value='Please delete your message, and send the bot a direct message with your '
                                  'command instead. This is in place to protect the privacy of our users.')
                return await ctx.send(embed=e)
        # Category does not exist?
        else:
            e = discord.Embed(color=values.DEFAULT_COLOR)
            e.add_field(name='That category does not exist!',
                        value='Please complete your registration using "!register" before running this command, '
                              'or contact us using "!mail [message]" if you are having issues.')
            return await ctx.send(embed=e)

        return await utils.dm(ctx.author, ctx, info, name='Server List')

    @commands.command(**values.Commands.INVITE)
    async def invite(self, ctx):
        default_url = 'https://discord.com/api/oauth2/authorize' \
                      '?client_id=843981504785809438' \
                      '&permissions={perms}' \
                      '&scope=bot'
        # TODO: Hex calculator for perms?
        msg_perms = default_url.format(perms='18432')
        role_perms = default_url.format(perms='268453888')
        e = discord.Embed(color=values.DEFAULT_COLOR)
        e.add_field(name='Invite UniFy to your server!',
                    value='[Send Messages only]({url})'.format(url=msg_perms) +
                          '\n[Manage Roles + Send Messages]({url})'.format(url=role_perms))

        return await ctx.send(embed=e)

    ######################
    #                    #
    #   OWNER COMMANDS   #
    #                    #
    ######################

    @servers.command(**values.Commands.SERVERS_UNIFY)
    @commands.is_owner()  # Only the bot owner may run this command c:
    @commands.dm_only()
    async def unify(self, ctx, *, message):
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
        # If category does not exist
        else:
            settings_data['servers'].update(data)
        write_settings('servers.json', domain, settings_data, mode='update')

        log('Server {name} added to servers.json!'.format(name=name))
        await utils.send_basic(ctx, title='Server "{name}" successfully added!'.format(name=name),
                               name='Domain: {0[0]}'.format(args),
                               value='''Category: {0[1]}
                                     Server ID: {0[2]}
                                     Name: {0[3]}
                                     Invite Link: {0[4]}
                                     Verified Role: {0[5]}'''.format(args))

    @blacklist.command(**values.Commands.BLACKLIST_BAN)
    @commands.is_owner()  # Only the bot owner may run this command c:
    @commands.dm_only()
    async def ban(self, ctx, user_id, *, reason=None):
        # TODO: Make a "Blacklisted" role and give them that?
        # Update the blacklist
        blacklisted = get_settings('users.json', 'blacklisted')
        blacklisted.append(user_id)
        write_settings('users.json', 'blacklisted', blacklisted)
        # Get the user's info
        blacklisted_user = await self.bot.fetch_user(user_id)

        e = discord.Embed(title='ALERT! User has been blacklisted!', description=blacklisted_user.mention,
                          color=discord.Colour.red())
        e.add_field(name='User ID: {.id}'.format(blacklisted_user),
                    value='Please either ban or remove all permissions from this user ASAP!')
        # Attempt to ban the blacklisted user from all servers
        # TODO: Remove 150 limit
        async for guild in self.bot.fetch_guilds(limit=150):
            try:
                await guild.ban(blacklisted_user, reason=reason)
            except discord.Forbidden:
                # Go through each channel and try sending it to the best one
                channel_list = await guild.fetch_channels()
                text_channels = [channel for channel in channel_list if isinstance(channel, discord.TextChannel)]
                # List of best channels to send the alert in
                best_channels = [
                    ['mod', 'admin'],
                    ['general']
                ]
                message_sent = False
                # Go through twice: It will try sending it to the best channel on the
                # first go, but if it can't, it will try sending it to any channel.
                for i in range(len(best_channels) + 1):
                    for channel in text_channels:
                        try:
                            # If it's the best channel, or it's our last run-through, send the alert
                            if i == len(best_channels) or any(name in channel.name for name in best_channels[i]):
                                await channel.send(embed=e)
                                message_sent = True
                                break
                        except discord.Forbidden as error:
                            log(error)
                            continue
                    if message_sent:
                        break

        log('User {user_id} has been BLACKLISTED!'.format(user_id=user_id))
        e = discord.Embed(title='User "{user_id}" has been BLACKLISTED!'.format(user_id=user_id),
                          color=values.DEFAULT_COLOR)
        return await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Servers(bot))
