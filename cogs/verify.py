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

from cogs.utils import utils, values
from cogs.utils.config import get_settings, write_settings
from cogs.utils.emailer import send_email
from cogs.utils.error_handler import log


class Verify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.char_list = string.ascii_letters + string.digits
        self._email_regex = '^[-!#$%&\'*+/0-9=?A-Z^_a-z{|}~](\\.?[-!#$%&\'*+/0-9=?A-Z^_a-z{|}~])*@[a-zA-Z](-?[' \
                            'a-zA-Z0-9])*(\\.[a-zA-Z](-?[a-zA-Z0-9])*)+$'
        # TODO: Replace 'contact the owner' with feature to request adding a university domain

    @commands.group(**values.Commands.REGISTER)
    async def register(self, ctx):
        # If the user runs a subcommand (like "!register code"), we need to let the subcommand run
        # without interruption. Simply calling "return" does just that.
        if ctx.invoked_subcommand is not None:
            return

        # Check if the user is already registered
        settings = get_settings('users.json', 'verified')
        if str(ctx.author.id) in settings.keys():
            already_verified = False
            e = discord.Embed(color=values.DEFAULT_COLOR, description=ctx.author.mention)
            e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            # Start going through the domain's categories
            user_domain = settings.get(str(ctx.author.id)).get('domain')
            server_categories = get_settings('servers.json', user_domain).get('servers')
            verified_server = None
            for category, servers in server_categories.items():
                # Go through each server
                guild = servers.get(str(ctx.guild.id))
                # If the server exists in the database
                if guild is not None:
                    verified_server = guild.get('name')
                    verified_role = guild.get('verified_role')
                    for role in ctx.guild.roles:
                        # If the stored role exists, attempt to give it to user
                        if verified_role == str(role.id) and verified_role is not None:
                            # Make sure they don't already have the role
                            if role in ctx.author.roles:
                                log('{.author} already has the Verified role!'.format(ctx))
                                already_verified = True
                                break
                            await ctx.author.add_roles(role, reason='User is registered with UniFy.')
            # Confirm that the user now has the role
            if already_verified:
                e.add_field(name='You already have the Verified role!',
                            value='If you are experiencing issues, please contact us using "!mail [message]".')
            else:
                log('Successfully verified {user} in {server}!'.format(user=ctx.author, server=verified_server))
                e.add_field(name='Verification successful!',
                            value='Thank you for using UniFy.')

            return await ctx.send(embed=e)

        # Upon running !register, send user a DM requesting their email address
        await utils.dm(ctx.author, ctx, values.REGISTER, name='Register with UniFy',
                       confirmation_msg='Registering {.author}...'.format(ctx))
        e = discord.Embed(color=values.DEFAULT_COLOR)  # Reset the embed

        def check(msg):
            return re.search(self._email_regex, msg.content) and msg.channel == ctx.author.dm_channel

        try:
            log('Waiting 60s for {.author}'.format(ctx))
            reply = await self.bot.wait_for('message', timeout=60.0, check=check)  # Wait 60s for their reply
        except asyncio.TimeoutError:
            log('Time expired for {.author}'.format(ctx))
            e.add_field(name='Time expired (60s).', value='Please type in a valid email before time runs out.')
        else:
            log('Successful email reply from {.author}'.format(ctx))
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
                               values.EMAIL_MESSAGE.format(author=ctx.author.name, id=ctx.author.id, code=code))
                    log('Email sent to {reply} at {time}.'.format(reply=reply.content, time=now))
                    e.add_field(name='Email sent!',
                                value='A verification code has been sent to {.content}. '.format(reply) +
                                      'Please check your email (including your spam folder) and type '
                                      'it here.')
                    e.add_field(name='Format:', value='!register code [insert code here]', inline=False)
                else:
                    e.add_field(name='User is already pending verification!',
                                value='A code has already been sent to you. Please complete your pending '
                                      'verification first with "!register code [insert code here]"')
            # If domain is not registered, inform the user
            # TODO: Add better university registering features in the future
            else:
                e.add_field(name='Invalid domain!',
                            value='Your domain @{domain} is not verified. '.format(domain=domain) +
                                  'Please enter an email address from a verified university domain, or contact '
                                  'us using "!mail {message}" to register your university with UniFy.')

        return await ctx.author.send(embed=e)

    @register.command(**values.Commands.REGISTER_CODE)
    @commands.dm_only()
    @commands.cooldown(5, 900.0, commands.BucketType.user)  # Once every 15m per user
    async def code(self, ctx, code):
        e = discord.Embed(color=values.DEFAULT_COLOR)

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
        for user, data in pending.items():
            # If the user exists
            if user == str(ctx.author.id):
                user_found = True
                # If verification period has not yet expired
                if floor(time.time()) - data.get('epoch_sent_at') <= 86400:  # 24 hours = 86'400 seconds
                    hashed_code = hashlib.sha512(code.encode('utf-8')).hexdigest()
                    # If their code matches what's in our database
                    if hashed_code == pending.get(user).get('hashed_code'):
                        # Update the users.json file
                        update_data = {
                            user: {
                                # "email": data.get('email'),
                                "domain": data.get('domain')
                            }
                        }
                        del_pending_user(user)
                        write_settings('users.json', 'verified', update_data, mode='update')
                        log('User {.author} successfully registered!'.format(ctx))
                        e.add_field(name='Registration successful!',
                                    value='You now have access to your domain\'s Discord servers!'
                                          '\nPlease type "!register" in the verification channel a second time'
                                          'to receive the Verified role!')
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


def setup(bot):
    bot.add_cog(Verify(bot))
