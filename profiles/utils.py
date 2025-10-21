"""
Defines utility classes and functions for managing user accounts.
"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()


class SpecialCharacterPasswordValidator:
    """
    Custom password validator to ensure special characters are used.
    """

    def validate(self, password, user=None):
        special_characters = '~`!@#$%^&*()-_=+[{]};:\'"<>/?'
        for character in password:
            if character in special_characters:
                break
            else:
                continue
        else:
            raise ValidationError(
                'Password must contain at least one special character',
                code='missing_special_character'
            )

    def get_help_text(self):
        return 'Your password must contain at least one special character.'


async def reset_password(email):
    """
    Sends a user an email with a link to reset their password.
    """
    try:
        user = await User.objects.aget(email=email)
    except:
        # If the user doesn't exist, do nothing.
        return
    else:
        await user.send_reset_password_email()
    return
