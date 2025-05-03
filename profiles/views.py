"""
Defines view functions for creating and managing user accounts.
"""

from django.contrib import auth, messages
from django.shortcuts import redirect, render

from profiles import forms


User = auth.get_user_model()


def login(request):
    context = {'form': forms.LoginForm()}
    return render(request, 'registration/login.html', context)


def create_user(request):
    if request.method == 'POST':
        form = forms.CreateUserForm(data=request.POST)
        if form.is_valid():
            user = User(
                username='',
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('add_mobile_number')
        errors = [text for value in form.errors.values() for text in value]
        for item in errors:
            messages.error(request, item)
    context = {'form': forms.CreateUserForm()}
    return render(request, 'registration/create_user.html', context)


def add_mobile_number(request):
    """
    Prompts a new user to add their mobile phone.
    """
    context = {'form': forms.MobileNumberForm()}
    return render(request, 'registration/add_mobile_number.html', context)
