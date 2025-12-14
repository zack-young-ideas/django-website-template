"""
Defines view functions for creating and managing user accounts.
"""

import asyncio

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from profiles import forms, models, utils


User = auth.get_user_model()


def login(request):
    if request.method == 'POST':
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(
                request,
                username=username,
                password=password
            )
            if (user is not None):
                auth.login(request, user)
                return redirect('dashboard')
    context = {'form': forms.LoginForm()}
    return render(request, 'login.html', context)


def forgotten_password(request):
    context = {'form': forms.ForgottenPasswordForm()}
    return render(request, 'forgotten_password.html', context)


async def sleeper():
    """
    Waits a fixed amount of time.
    """
    await asyncio.sleep(3)


async def forgotten_password_handler(request):
    if request.method == 'POST':
        form = forms.ForgottenPasswordForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first, second = await asyncio.gather(
                sleeper(),
                utils.reset_password(email=email)
            )
            return redirect('forgotten_password_confirmation')
    raise Http404()


def forgotten_password_confirmation(request):
    return render(request, 'forgotten_password_confirmation.html')


def reset_password(request, email_token):
    try:
        user = models.ResetPasswordToken.objects.check_token(
            token=email_token
        )
    except models.ResetPasswordToken.DoesNotExist:
        raise Http404()
    else:
        if request.method == 'POST':
            form = forms.ResetPasswordForm(data=request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                return redirect('reset_password_confirmation')
        context = {
            'form': forms.ResetPasswordForm(),
            'token': email_token
        }
        return render(request, 'reset_password.html', context)


def reset_password_confirmation(request):
    return render(request, 'reset_password_confirmation.html')


def create_user(request):
    if request.method == 'POST':
        form = forms.CreateUserForm(data=request.POST)
        if form.is_valid():
            user = User(email=form.cleaned_data['email'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            auth.login(request, user)
            return redirect('add_mobile_number')
        errors = [text for value in form.errors.values() for text in value]
        for item in errors:
            messages.error(request, item)
    context = {'form': forms.CreateUserForm()}
    return render(request, 'registration/create_user.html', context)


@login_required
def add_mobile_number(request):
    """
    Prompts a new user to add their mobile phone.
    """
    if request.method == 'POST':
        form = forms.MobileNumberVerificationForm(data=request.POST)
        if form.is_valid():
            sms_token = form.cleaned_data['sms_token']
            if request.user.check_sms_token(sms_token):
                request.user.create_email_token()
                return redirect('create_user_success')
            else:
                messages.error(request, 'Invalid SMS code.')
    context = {'form': forms.MobileNumberVerificationForm()}
    return render(request, 'registration/add_mobile_number.html', context)


@login_required
def create_user_success(request):
    """
    Prompts a new user to follow the link in the email sent to them.
    """
    return render(request, 'registration/create_user_success.html')


def email_verification(request, verification_token):
    """
    The link a user must follow in order to verify their email address.
    """
    form = forms.EmailVerificationTokenForm({
        'verification_token': verification_token
    })
    if form.is_valid():
        try:
            verification_token = form.cleaned_data['verification_token']
            email_token = models.EmailToken.objects.check_token(
                token=verification_token
            )
        except models.EmailToken.DoesNotExist:
            raise Http404()
        else:
            return render(
                request,
                'registration/email_verification_success.html'
            )


@login_required
def dashboard(request):
    return render(request, 'registration/dashboard.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')
