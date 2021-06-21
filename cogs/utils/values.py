import discord

DEFAULT_COLOR = discord.Colour.orange()

ISSUES = 'If you are experiencing issues, please contact us using "!mail [message]".'
HELP = 'Please type "!help [command]" for more information'

REGISTER = ('To register with UniFy, please type in your *university email address*.'
            '\n\n**Your email is not stored by UniFy**. Your privacy and security are our '
            'utmost priority, so your address is only used for the registration process to '
            'confirm that you are a university student, and will *never be shared with '
            'anyone. For more details, please see UniFy\'s Privacy Policy.'
            '\n\nPlease note that UniFy will only register users with a valid '
            'university email. If your university\'s domain is not in our database, '
            'please contact us using "!mail [message]" to have it added.')
EMAIL_MESSAGE = ('Thank you for registering with UniFy!'
                 '\nIf you did not initiate this request, please ignore this message.\n'
                 # '\nUsername: {author}'
                 # '\nDiscord ID: {id}'
                 '\nVerification Code: {code}\n'
                 '\nTo finish registering, type "!register code [code]" before the code '
                 'expires in 24 hours.')
INVALID_DOMAIN = ('Your domain @{domain} is not verified.'
                  '\nPlease enter an email address from a verified university domain, '
                  'or contact us using "!mail [message]" to register your university with UniFy.')
REPLY_EXPIRED = 'Please type in a valid email before time runs out.'
VERIFICATION_EXPIRED = 'Please try again, and complete the verification process before 24 hours.'

# TODO: Clean up this shit omfg

SERVERS_INVALID_USER_ID = {
    'name': 'Invalid User ID!',
    'value': HELP
}
SERVERS_INVALID_SERVER_ID = {
    'name': 'Invalid Server ID!',
    'value': HELP
}
SERVERS_INVALID_INVITE = {
    'name': 'Invalid Invite Link!',
    'value': HELP
}
SERVERS_INVALID_VERIFIED_ROLE = {
    'name': 'Invalid Verified Role ID!',
    'value': HELP
}
SERVERS_INVALID_CATEGORY = {
    'name': 'That category does not exist!',
    'value': 'Please check the spelling (and capitalization) of the category, and try again.'
}
INCORRECT_ARGUMENT = {
    'name': 'Invalid argument passed into the command!',
    'value': 'Please type "!help [command] and try again.'
}


class Commands:
    REGISTER = {
        'description': 'Register yourself with UniFy.',
        'usage': '- to begin the registration process, '
                 '\n!register code [code] - to input your verification code (in DMs only), '
                 '\n!register - again to confirm your registration and receive the verified role '
                 '(in the #verification server channel).',
        'invoke_without_subcommand': True
    }
    REGISTER_CODE = {
        'description': 'Input the verification code sent to your email to register with UniFy',
        'usage': '[code]'
    }

    SERVERS = {
        'aliases': ['server']
    }
    SERVERS_REQUEST = {
        'description': 'Request to have a server added to the database. A verified role must exist.'
                       '\nPlease enable Discord\'s Developer Mode before proceeding.'
                       '\n*Make sure to include the commas!*'
                       '\n\nTo get your server ID, right-click your server icon and select "Copy ID".'
                       '\nTo get a permanent invite, click on your server name and select "Invite '
                       'People". Next, select "Edit invite link", select "EXPIRE AFTER: Never" '
                       'and "MAX NUMBER OF USES: No Limit", then "Generate a New Link", then "Copy".'
                       '\nTo get your verified role ID, click on your server name and navigate to '
                       'Server Settings > Roles. If you do not have a Verified role, create one. '
                       'If you do, hover over it, select "More", then "Copy ID".',
        'usage': '[server ID], [name], [permanent invite], [Verified role ID]'
    }
    SERVERS_UNIFY = {
        'description': 'Add a server to the database.',
        'usage': '[domain] ["category"] [server ID] ["name"] [permanent invite] [ID of "verified role"]'
    }
    SERVERS_LIST = {
        'description': '',
        'usage': ''
    }

    BLACKLIST = {}
    BLACKLIST_APPEAL = {
        'description': 'Appeal to blacklist a user from all registered servers.'
                       '\nPlease enable Discord\'s Developer Mode before proceeding.'
                       '\n\nTo get the user\'s ID, right-click their profile picture or name and '
                       'select "Copy ID".',
        'usage': '[user ID] [reason (optional but very recommended)]'
    }
    BLACKLIST_BAN = {
        'description': 'Blacklist a user from all university Discords.',
        'usage': '[User ID] [reason (defaults to None)]'
    }

    INVITE = {}

    FAQ = {
        'aliases': ['questions'],
        'description': 'Gives information about commonly asked questions.'
    }
    MAIL = {
        'description': 'Message the owner of this bot.',
        'usage': '[message goes here]'
    }


class Faq:
    EMAIL_WORRY = {
        'name': 'I don\'t like having to use my university email address. Do I need it to register?',
        'value': '__**Yes.**__ Your privacy and safety are our biggest concerns, which is why we spent weeks '
                 'coming up with the best way for students to safely register. Confirming your university '
                 'email does just that. The registration process is secure, it\'s fully private, and no one '
                 'will have access to it except *you*. Not even *the university*. If that isn\'t enough, '
                 'any and all data collected by UniFy will *never be shared with anyone*.',
        'inline': False
    }
    BENEFITS = {
        'name': 'What are the benefits of registering with UniFy?',
        'value': 'You will gain access to the list of verified university servers, ranging from your '
                 'classes, to student hubs, to social groups. In addition, each server registered with '
                 'UniFy will have a "Verified" role, and you will gain access to one or more perks '
                 'provided by the server\'s owner, depending on the level of security.',
        'inline': False
    }
    WHY_MAKE_IT = {
        'name': 'Why did you make UniFy?',
        'value': 'I want to make Discord a safer platform for university students. Finding my class '
                 'servers is always a challenge, so I want to make it a seamless experience to help '
                 'with online learning. I added a verification process to help prevent raids, since '
                 'I\'m tired of constantly having to drop everything I\'m doing to spend an hour '
                 'alerting other mods, banning the raiders from all of my classes, and removing very, '
                 '*very* disturbing images from my channels. Hopefully, UniFy accomplishes all of '
                 'that and more.',
        'inline': False
    }
    CONTACT = {
        'name': 'My question isn\'t on here. How can I contact you for any questions/comments/insults?',
        'value': 'Please use the "!mail [message]" command if you need help with a bug, have an awesome '
                 'idea for a new feature, or anything else! We made this bot for *you guys*, so we\'re '
                 'open to feedback and suggestions 24/7.',
        'inline': False
    }


class Errors:
    NOT_REGISTERED = {
        'name': 'You are not registered with UniFy!',
        'value': 'Please complete your registration using "!register" before running this command. ' + ISSUES
    }
    DM_ONLY = {
        'name': 'This command can only be run in DMs!',
        'value': 'Please delete your message, and send the bot a Direct Message with your command instead.'
    }
    GUILD_ONLY = {
        'name': 'This command cannot be run in DMs!',
        'value': 'Please run this command in a server with UniFy.'
    }

    COMMAND_NOT_FOUND = {
        'name': 'Command not found!',
        'value': 'Please confirm you are trying to run a valid command, and try again.'
    }
    MISSING_ARGUMENT = {
        'name': 'Command is missing a required argument!',
        'value': HELP
    }
    INVALID_ARGUMENT = {
        'name': 'Invalid '
    }
    FORBIDDEN = {
        'name': 'The bot was prevented from executing the command!',
        'value': 'Please temporarily allow Direct Messages from other server members, and try again.'
    }
    # HTTP_EXCEPTION = {
    #     'name': 'Something went wrong!',
    #     'value': ISSUES
    # }
    EXPIRED_TOKEN = {
        'name': 'Email could not be sent (token is expired)!',
        'value': 'Please contact us using "!mail [message]" so we can refresh the OAuth2 token.'
    }
    OTHER = {
        'name': 'There was an error!',
        'value': ISSUES
    }

    # INVALID_SUBCOMMAND = {
    #     'name': 'Invalid subcommand!',
    #     'value': 'Please type "!help {.command}" to get started.'
    # }
