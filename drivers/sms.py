"""
Defines tools for sending SMS messages.
"""

from django.conf import settings
from django.utils.module_loading import import_string


def get_connection(backend=None, **kwargs):
    """
    Load an SMS backend and return an instance of it.
    """
    klass = import_string(backend or settings.SMS_BACKEND)
    return klass(**kwargs)


def send_sms_message(message, recipient_number):
    """
    Uses SMS backend to send message to specified number.
    """
    sms = get_connection()
    return sms.send_message(message, recipient_number)
