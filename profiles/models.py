"""
Defines models that are used to create and manage user accounts.
"""

import datetime
import secrets
import string

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from drivers import send_sms_message


class User(AbstractBaseUser):

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'

    def add_new_mobile_number(self, mobile_number):
        """
        Creates a new PhoneToken object and sends SMS code.
        """
        token_object = PhoneToken(
            phone=mobile_number,
            user=self
        )
        token_object.save()

    def check_sms_token(self, sms_token):
        """
        Checks that the code submitted by the user is correct.
        """
        phonetoken_object = self.phonetoken_set.last()
        if phonetoken_object.is_current():
            return check_password(
                sms_token,
                phonetoken_object.token
            )
        else:
            return False

    def add_email_address(self, email_address):
        """
        Updates a user's email address and sends a verification link.
        """
        token_object = EmailToken(
            email=email_address,
            user=self
        )
        token_object.save()


class PhoneToken(models.Model):

    token = models.CharField(max_length=256)
    phone = models.CharField(max_length=12)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    failed_attempts = models.SmallIntegerField(default=0)

    def _generate_token(self):
        """
        Creates a unique 6-digit numeric code.
        """
        if not self.token:
            token = ''.join(
                secrets.choice(string.digits) for i in range(6)
            )
        return token

    def _send_sms_message(self, token, mobile_number):
        """
        Sends an SMS message to the given phone number with the token.
        """
        sms_message = 'Your mobile verification code is {0}.'
        send_sms_message(
            sms_message.format(token),
            mobile_number
        )

    def save(self, *args, **kwargs):
        token = self._generate_token()
        self.token = make_password(token)
        self._send_sms_message(token, self.phone)
        models.Model.save(self, *args, **kwargs)

    def is_current(self):
        """
        Returns True if email token was created less than 1 hour ago.
        """
        time_difference = timezone.now() - self.datetime
        one_hour = datetime.timedelta(hours=1)
        return one_hour > time_difference


class CustomEmailTokenManager(models.Manager):

    def check_token(self, token):
        """
        Checks to see whether the given token exists.
        """
        email_token_objects = self.all()
        token_exists = False
        for email_token_object in email_token_objects:
            token_exists = check_password(
                token,
                email_token_object.token
            )
            if token_exists:
                return email_token_object
        raise EmailToken.DoesNotExist


class EmailToken(models.Model):

    token = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    failed_attempts = models.SmallIntegerField(default=0)

    objects = CustomEmailTokenManager()

    def _generate_token(self):
        """
        Creates a unique 32-character string.
        """
        alphabet = string.ascii_uppercase + string.ascii_lowercase
        alphabet += string.digits
        if not self.token:
            token = ''.join(
                secrets.choice(alphabet) for i in range(32)
            )
        return token

    def _send_email(self, token, email_address):
        """
        Sends a verification link to a user via email.
        """
        # First, determine the URL for the verification link.
        verification_url = reverse(
            'email_verification',
            kwargs={'verification_token': token}
        )
        # Next, define the default text for the email.
        default_text = ('Please confirm your email address '
                        'by clicking the link below.\n\n'
                        '{0}://{1}{2}')
        text_email_message = default_text.format(
            settings.SCHEME,
            settings.DOMAIN,
            verification_url
        )
        # Then, render the HTML content of the email.
        template_context = {
            'scheme': settings.SCHEME,
            'domain': settings.DOMAIN,
            'path': verification_url,
        }
        html_email_message = render_to_string(
            'email_verification.html',
            template_context
        )
        # Finally, send the email.
        send_mail(
            'Verify Email Address',
            text_email_message,
            'noreply@{0}'.format(settings.DOMAIN),
            [email_address],
            fail_silently=False,
            html_message=html_email_message
        )

    def save(self, *args, **kwargs):
        token = self._generate_token()
        self.token = make_password(token)
        self._send_email(token, self.email)
        models.Model.save(self, *args, **kwargs)

    def is_current(self):
        """
        Returns True if email token was created less than 1 hour ago.
        """
        time_difference = timezone.now() - self.datetime
        one_hour = datetime.timedelta(hours=1)
        return one_hour > time_difference
