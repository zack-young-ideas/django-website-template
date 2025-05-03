"""
Defines SMS backend that stores messages in memory.
"""

from drivers import sms


class Message:

    def __init__(self, message, recipient_number):
        self.message = message
        self.recipient = recipient_number


class SmsBackend:

    def __init__(self, *args, **kwargs):
        """
        Stores all delivered SMS messages in a list.
        """
        if not hasattr(sms, 'messages'):
            sms.messages = []

    def send_message(self, message, recipient_number):
        """
        Redirect message to dummy outbox list.
        """
        sms.messages.append(Message(message, recipient_number))
