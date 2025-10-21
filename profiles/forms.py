"""
Defines forms for creating and managing user accounts.
"""

from django import forms
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from phonenumber_field.formfields import PhoneNumberField


class LoginForm(forms.Form):

    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }
        )
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
    )


def validate_secret_key(value):
    """
    Ensures that the correct secret key was entered.
    """
    if value != settings.SECRET_SAUCE:
        raise ValidationError('That\'s not the secret sauce.')


class CreateUserForm(forms.Form):

    first_name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }
        )
    )
    last_name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }
        )
    )
    password = forms.CharField(
        label='',
        validators=[validate_password],
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
    )
    confirm_password = forms.CharField(
        label='',
        validators=[validate_password],
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password'
            }
        )
    )
    secret_key = forms.CharField(
        label='',
        validators=[validate_secret_key],
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Secret Sauce'
            }
        )
    )

    def clean(self):
        """
        Ensures that passwords match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error(
                'password',
                ValidationError('Passwords do not match.')
            )


class MobileNumberForm(forms.Form):

    mobile_number = PhoneNumberField(
        label='',
        label_suffix='',
        region='CA',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Mobile Number'
            }
        )
    )


class MobileNumberVerificationForm(MobileNumberForm):

    sms_token = forms.CharField(
        label='',
        min_length=6,
        max_length=6,
        validators=[RegexValidator(
            regex=r'^\d{6}$',
            message='Invalid SMS token.'
        )],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control hide',
                'placeholder': 'SMS Token',
                'style': 'display:none;',
            }
        )
    )


class EmailForm(forms.Form):

    email = forms.EmailField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }
        )
    )
    confirm_email = forms.EmailField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Email'
            }
        )
    )

    def clean(self):
        """
        Ensures that email addresses match.
        """
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')
        if email != confirm_email:
            self.add_error(
                'email',
                ValidationError('Email addresses do not match.')
            )


class EmailVerificationTokenForm(forms.Form):

    verification_token = forms.CharField(
        min_length=32,
        max_length=32,
        validators=[RegexValidator(
            regex=r'^[A-Za-z0-9]{32}$',
            message='Invalid email token.'
        )]
    )


class ForgottenPasswordForm(forms.Form):

    email = forms.EmailField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }
        )
    )


class ResetPasswordForm(forms.Form):

    password = forms.CharField(
        label='',
        validators=[validate_password],
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
    )
    confirm_password = forms.CharField(
        label='',
        validators=[validate_password],
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password'
            }
        )
    )

    def clean(self):
        """
        Ensures that passwords match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error(
                'password',
                ValidationError('Passwords do not match.')
            )
