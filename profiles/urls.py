from django.urls import path, re_path

from profiles import views

urlpatterns = [
    path('login', views.login, name='login'),
    path(
        'forget/password', 
        views.forgotten_password, 
        name='forgotten_password'
    ),
    path(
        'forget/password/handler', 
        views.forgotten_password_handler, 
        name='forgotten_password_handler'
    ),
    path(
        'forget/password/confirmation', 
        views.forgotten_password_confirmation, 
        name='forgotten_password_confirmation'
    ),
    path(
        'reset/password/confirmation',
        views.reset_password_confirmation,
        name='reset_password_confirmation',
    ),
    path(
        'reset/password/<str:email_token>',
        views.reset_password,
        name='reset_password',
    ),
    path('create', views.create_user, name='create_user'),
    path('create/phone', views.add_mobile_number, name='add_mobile_number'),
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
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
]
