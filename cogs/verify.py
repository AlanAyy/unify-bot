import asyncio
import json
import re
import time

import string
import secrets
import hashlib
from math import floor

import discord
from discord.ext import commands
from discord.ext.commands import group
from cogs.utils.config import get_settings, write_settings
from cogs.utils.email_util import send_email
from cogs.utils.embeds import DEFAULT_COLOUR


class Verify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.char_list = string.ascii_letters + string.digits
        self._email_regex = '^[-!#$%&\'*+/0-9=?A-Z^_a-z{|}~](\\.?[-!#$%&\'*+/0-9=?A-Z^_a-z{|}~])*@[a-zA-Z](-?[' \
                            'a-zA-Z0-9])*(\\.[a-zA-Z](-?[a-zA-Z0-9])*)+$'
        # TODO: Replace 'contact the owner' with feature to request adding a university domain
        self._register_message = ('To register with UniFy, please type in your email address. \nWe will only use '
                                  'this information to confirm that you are a university student, and it will '
                                  '*never be shared with anyone*. For more details, please see UniFy\'s Privacy '
                                  'Policy. \nPlease note that UniFy will only register users with a valid '
                                  'university email. If your university\'s domain is not in our database, '
                                  'please contact us using "!mail {message}" to have it added.')
        self._email_message = ('Thank you for registering with UniFy!'
                               '\nIf you did not initiate this request, please ignore this message.\n'
                               # '\nUsername: {author}'
                               # '\nDiscord ID: {id}'
                               '\nVerification Code: {code}\n'
                               '\nTo finish registering, type "!register code {code}" before the code '
                               'expires in 24 hours.')

    @group(description='Register yourself with UniFy.',
           invoke_without_subcommand=True)
    async def register(self, ctx):
        # TODO: Check for repeat code inputs to prevent brute-force possibilities
        # TODO: Check for repeat emails that are already verified

        # If the user runs a subcommand (like "!register code"), we need to let the subcommand run
        # without interruption. Simply calling "return" does just that.
        if ctx.invoked_subcommand is not None:
            return

        # Check if the user is already registered
        settings = get_settings('users.json', 'verified')
        role_found = False
        if str(ctx.author.id) in settings.keys():
            # Embed magic c:
            e = discord.Embed(color=DEFAULT_COLOUR, description=ctx.author.mention)
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            # Start going through the domain's categories
            user_domain = settings.get(str(ctx.author.id)).get('domain')
            server_categories = get_settings('servers.json', user_domain).get('servers')
            for category, servers in server_categories.items():
                # Go through each server
                guild = servers.get(str(ctx.guild.id))
                # If the server exists in the database
                if guild is not None:
                    verified_role = guild.get('verified_role')
                    for role in ctx.guild.roles:
                        # If the stored role exists, attempt to give it to user
                        if verified_role == str(role.id) and verified_role is not None:
                            role_found = True
                            await ctx.author.add_roles(role, reason='Verified')
                            e.add_field(name='Verified role applied!',
                                        value='If you are experiencing issues with accessing '
                                              'servers, please contact us using "!mail {message}"')
                            break
                if role_found:
                    break
            # TODO: Cover edge case where user does not get role but also does not get message
            if not role_found:
                e.add_field(name='You are already registered!',
                            value='If you are experiencing issues with accessing '
                                  'servers, please contact us using "!mail {message}".')
            return await ctx.send(embed=e)

        # Upon running !register, send user a DM requesting their email address
        e = discord.Embed(color=DEFAULT_COLOUR)
        e.add_field(name='Register with UniFy', value=self._register_message)
        await ctx.author.send(embed=e)
        e = discord.Embed(color=DEFAULT_COLOUR)  # Reset the embed

        def check(msg):
            return re.search(self._email_regex, msg.content) and msg.channel == ctx.author.dm_channel

        try:
            print('Waiting 60s for {.author}'.format(ctx))
            reply = await self.bot.wait_for('message', timeout=60.0, check=check)  # Wait 60s for their reply
        except asyncio.TimeoutError:
            print('Time expired for {.author}'.format(ctx))
            e.add_field(name='Time expired (60s).', value='Please type in a valid email before time runs out.')
        else:
            print('Successful email reply from {.author}'.format(ctx))
            # Read JSON domain
            email, domain = reply.content.split('@')
            verified_unis = get_settings('config.json', 'verified_unis')
            pending = get_settings('users.json', 'pending')
            # Check if it's a valid domain and user is not already pending registration
            if domain in verified_unis.values():
                if str(ctx.author.id) not in pending.keys():
                    # Generate, hash and store secret code
                    code = ''.join(secrets.choice(self.char_list) for _ in range(8))  # Generate a code 8 chars long
                    hashed_code = hashlib.sha512(code.encode('utf-8')).hexdigest()  # Hash
                    now = floor(time.time())
                    data = {
                        str(ctx.author.id): {
                            "email": email,
                            "domain": domain,
                            "epoch_sent_at": now,
                            "hashed_code": hashed_code
                        }
                    }
                    write_settings('users.json', 'pending', data, mode='update')  # Store
                    # Send the email with the code, and inform the user on how to confirm it.
                    send_email(reply.content, 'UniFy Verification Code',
                               self._email_message.format(author=ctx.author.name, id=ctx.author.id, code=code))
                    print('Email sent to {reply} at {time}.'.format(reply=reply.content, time=now))
                    e.add_field(name='Email sent!',
                                value='A verification code has been sent to {.content}. '.format(reply) +
                                      'Please check your email (including your spam folder) and type '
                                      'it here.')
                    e.add_field(name='Format:',
                                value='!register code {insert code here}')
                else:
                    e.add_field(name='User is already pending verification!',
                                value='A code has already been sent to you. Please complete your pending '
                                      'verification first with "!register code {insert code here}"')
            # If domain is not registered, inform the user
            # TODO: Add better university registering features in the future
            else:
                e.add_field(name='Invalid domain!',
                            value='Your domain @{domain} is not verified. '.format(domain=domain) +
                                  'Please enter an email address from a verified university domain, or contact '
                                  'us using "!mail {message}" to register your university with UniFy.')

        return await ctx.author.send(embed=e)

    @register.command(description='Input the verification code sent to your email to register with UniFy',
                      usage='{code}')
    @commands.dm_only()
    async def code(self, ctx, code):
        e = discord.Embed(color=DEFAULT_COLOUR)

        def del_pending_user(user_to_delete):
            with open('settings/users.json', 'r+') as fpd:
                users_data = json.load(fpd)
                pending_user = users_data.get('pending')
                del pending_user[user_to_delete]
                fpd.seek(0)
                fpd.truncate()
                json.dump(users_data, fpd, indent=2)

        # Check if the user is pending verification
        pending = get_settings('users.json', 'pending')
        user_found = False
        for user, values in pending.items():
            # If the user exists
            if user == str(ctx.author.id):
                user_found = True
                # If verification period has not yet expired
                if floor(time.time()) - values.get('epoch_sent_at') <= 86400:  # 24 hours = 86'400 seconds
                    hashed_code = hashlib.sha512(code.encode('utf-8')).hexdigest()
                    # If their code matches what's in our database
                    if hashed_code == pending.get(user).get('hashed_code'):
                        # Update the users.json file
                        data = {
                            user: {
                                "email": values.get('email'),
                                "domain": values.get('domain')
                            }
                        }
                        del_pending_user(user)
                        write_settings('users.json', 'verified', data, mode='update')
                        e.add_field(name='Verification successful!',
                                    value='You now have access to your domain\'s Discord servers!')
                    else:
                        e.add_field(name='Incorrect code!',
                                    value='Please try again.')
                else:
                    del_pending_user(user)
                    e.add_field(name='Verification period expired!',
                                value='Please try again, and complete the verification process before 24 hours.')
                # User has been found, so we can stop looking for em
                break
        # User not found?
        if not user_found:
            e.add_field(name='User is not pending verification!',
                        value='Type "!register" to get started.')

        return await ctx.author.send(embed=e)

    ######################
    #                    #
    #   ERROR-HANDLING   #
    #                    #
    ######################

    @register.error
    async def register_error(self, ctx, error):
        e = discord.Embed(color=DEFAULT_COLOUR)
        if isinstance(error, commands.CommandInvokeError):
            e.add_field(name='DM could not be sent!',
                        value='Please temporarily allow Direct Messages from other server members '
                              'to continue with the registration process.')
            print(error)
        else:
            raise error

        return await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Verify(bot))
