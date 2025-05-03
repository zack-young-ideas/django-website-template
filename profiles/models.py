"""
Defines models that are used to create and manage user accounts.
"""

import datetime
import secrets
import string

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


User = get_user_model()


class PhoneToken(models.Model):

    token = models.CharField(max_length=6)
    phone = models.CharField(max_length=12)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    failed_attempts = models.SmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = ''.join(
                secrets.choice(string.digits) for i in range(6)
            )
        models.Model.save(self, *args, **kwargs)

    def is_current(self):
        """
        Returns True if email token was created less than 1 hour ago.
        """
        time_difference = timezone.now() - self.datetime
        one_hour = datetime.timedelta(hours=1)
        return one_hour > time_difference
