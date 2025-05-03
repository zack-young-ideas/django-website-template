"""
Defines utility classes and functions for managing user accounts.
"""

from django.core.exceptions import ValidationError


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
