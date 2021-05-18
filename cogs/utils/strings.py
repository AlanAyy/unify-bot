class Info:
    RULES = ''


class Verify:
    class Names:
        REGISTER = 'Register with UniFy'

    class Values:
        CHECK_EMAIL = ''

        INVALID_DOMAIN = ('Your domain @{domain} is not verified.'
                          '\nPlease enter an email address from a verified university domain, '
                          'or contact us using "!mail {message}" to register your university with UniFy.')
        REPLY_EXPIRED = 'Please type in a valid email before time runs out.'
        VERIFICATION_EXPIRED = 'Please try again, and complete the verification process before 24 hours.'


class Errors:
    ISSUES = 'If you are experiencing issues, please contact us using "!mail {message}".'
