from discord.ext import commands

from cogs.utils.config import get_settings
from cogs.utils import messaging


class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Message the owner of this bot.',
                      usage='{text message here}')
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
    bot.add_cog(Misc(bot))
