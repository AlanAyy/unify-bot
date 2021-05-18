import logging
import os

from discord.ext import commands

from cogs.utils.config import *


# First time run config
def wizard():
    config = {}
    print('Welcome to AlanAyy\'s UniFy setup!')
    print('Please enter the bot\'s token:')
    config['discord_token'] = input('| ').strip().strip('"')

    print('\nPlease enter the bot\'s command prefix:')
    config['prefix'] = input('| ').strip()

    input('\nThank you! Let\'s start this up, shall we?')
    with open('settings/config.json', encoding='utf-8', mode='w') as f:
        json.dump(config, f, sort_keys=True, indent=4)


try:
    # Let's see if we've got a valid token and config file
    with open('settings/config.json', encoding='utf-8', mode='r') as fp:
        json.load(fp)
except IOError:
    wizard()

# Now that all the setup's finished, we're good to go!
logging.basicConfig(level=logging.INFO)
bot = commands.Bot(
    command_prefix=get_settings('config.json', 'prefix'),
    description='''UniFy, the Discord Bot made to help students connect with each other.
                \nMade by AlanAyy'''
)

# Time to load our modules :D
if __name__ == '__main__':
    for extension in os.listdir("cogs"):
        if extension.endswith('.py'):
            try:
                bot.load_extension("cogs." + extension[:-3])
            except Exception as e:
                print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))


@bot.event
async def on_ready():
    print('\nLogged in as %s' % bot.user)
    print('Bot ID is %s' % bot.user.id)


bot.run(get_settings('config.json', 'discord_token'))
