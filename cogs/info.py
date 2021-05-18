import discord
from discord.ext import commands

from cogs.utils.config import get_settings
from cogs.utils import messaging
from cogs.utils.discord_values import DEFAULT_COLOR


class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['questions'],
                      description='Gives information about commonly asked questions.')
    @commands.cooldown(1, 1800.0, commands.BucketType.guild)  # Once every 30m per guild
    async def faq(self, ctx):
        e = discord.Embed(title='UniFy FAQ (Frequently Asked Questions)', color=DEFAULT_COLOR)
        e.add_field(name='I don\'t like having to use my university email address. Do I need it to register?',
                    value='__**Yes.**__ Your privacy and safety are our biggest cocnerns, which is why we spent weeks '
                          'coming up with the best way for students to safely register. Confirming your university '
                          'email does just that. The registration process is secure, it\'s fully private, and no one '
                          'will have access to it except *you*. Not even *the university*. If that isn\'t enough, '
                          'any and all data collected by UniFy will *never be shared with anyone*.', inline=False)
        e.add_field(name='What are the benefits of registering with UniFy?',
                    value='You will gain access to the list of verified university servers, ranging from your '
                          'classes, to student hubs, to social groups. In addition, each server registered with '
                          'UniFy will have a "Verified" role, and you will gain access to one or more perks '
                          'provided by the server\'s owner, depending on the level of security.', inline=False)
        e.add_field(name='Why did you make UniFy?',
                    value='I want to make Discord a safer platform for university students. Finding my class '
                          'servers is always a challenge, so I want to make it a seamless experience to help '
                          'with online learning. I added a verification process to help prevent raids, since '
                          'I\'m tired of constantly having to drop everything I\'m doing to spend an hour '
                          'alerting other mods, banning the raiders from all of my classes, and removing very, '
                          '*very* disturbing images from my channels. Hopefully, UniFy accomplishes all of '
                          'that and more.', inline=False)
        e.add_field(name='My question isn\'t on here. How can I contact you for any questions/comments/insults?',
                    value='Please use the "!mail {message}" command if you need help with a bug, have an awesome '
                          'idea for a new feature, or anything else! We made this bot for *you guys*, so we\'re '
                          'open to feedback and suggestions 24/7.', inline=False)
        return await ctx.send(embed=e)

    @commands.command(description='Message the owner of this bot.',
                      usage='{message goes here}')
    async def mail(self, ctx, *, message):
        # Get owner ID
        owner_id = get_settings('config.json', 'owner_id')
        me = await self.bot.fetch_user(owner_id)

        await messaging.dm(me, ctx, name='Mail', message=message, confirmation_msg='Message sent!')

        #       Messaging time
        # e = discord.Embed(color=discord.Colour.orange(), description=ctx.author.mention)
        # e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        # e.add_field(name='Mail', value=message)

        # await me.send(embed=e)

        # e = discord.Embed(title='Message sent!', color=discord.Colour.orange(), description=ctx.author.mention)
        # return await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Info(bot))
