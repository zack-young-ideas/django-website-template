from django.urls import path, re_path

from profiles import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('create', views.create_user, name='create_user'),
    path('create/phone', views.add_mobile_number, name='add_mobile_number'),
    path('create/email', views.add_email, name='add_email'),
    path(
        'create/success',
        views.create_user_success,
        name='create_user_success'
    ),
    re_path(
        'email/verify/(?P<verification_token>[A-Za-z0-9]{32})',
        views.email_verification,
        name='email_verification'
    ),
]
