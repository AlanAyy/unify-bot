import random

import discord
from discord.ext import commands


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Roll dice. (Ex: !roll 2d6)',
                      usage='[n]d[s] - [n] is the # of dice, and [s] is the # of sides.')
    async def roll(self, ctx, dice):
        dice_amount, dice_type = [int(i) for i in dice.split('d')]
        rolls = [random.randint(1, dice_type) for _ in range(dice_amount)]

        e = discord.Embed(title='%s\'s Rolls' % ctx.author, colour=0xffffff)
        e.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        e.add_field(name='Total', value=str(sum(rolls)))
        e.add_field(name='Rolls', value='%s' % ', '.join(map(str, rolls)))

        return await ctx.send(embed=e)

    @commands.command(aliases=['donate', 'support', 'thanks'],
                      description='Help support the bot! <3')
    async def coffee(self, ctx):
        # TODO: Give people a way to donate to me for supporting this bot or smth lol
        e = discord.Embed(color=discord.Colour.orange())
        e.add_field(name='Thank you!',
                    value='I\'m gonna be honest, I just finished writing most of the bot\'s code so I\'m '
                          'a bit tired lol. I\'ll implement a proper way to support UniFy soon enough or something, '
                          'either through Patreon or whatever. If you wanna donate to make sure UniFy sticks '
                          'around for a while, send me a DM using "!mail {message}" and I\'ll go set something up. '
                          'Something as small as $2 will help me cover part of the costs, or buying me a small '
                          'coffee would really warm my heart and keep me motivated to add even more features in '
                          'the future. Until then, I\'m gonna go take a big nap. My brain is friiiied.')

        return await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Fun(bot))
