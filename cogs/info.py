import discord
from discord.ext import commands

from cogs.utils.config import get_settings
from cogs.utils import utils, values


class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(**values.Commands.FAQ)
    @commands.cooldown(1, 1800.0, commands.BucketType.guild)  # Once every 30m per guild
    async def faq(self, ctx):
        e = discord.Embed(title='UniFy FAQ (Frequently Asked Questions)', color=values.DEFAULT_COLOR)
        e.add_field(**values.Faq.EMAIL_WORRY)
        e.add_field(**values.Faq.BENEFITS)
        e.add_field(**values.Faq.WHY_MAKE_IT)
        e.add_field(**values.Faq.CONTACT)
        return await ctx.send(embed=e)

    @commands.command(**values.Commands.MAIL)
    async def mail(self, ctx, *, message):
        # Get owner ID
        owner_id = get_settings('config.json', 'owner_id')
        me = await self.bot.fetch_user(owner_id)

        await utils.dm(me, ctx, name='Mail', message=message, confirmation_msg='Message sent!')


def setup(bot):
    bot.add_cog(Info(bot))
