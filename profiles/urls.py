from django.urls import path

from profiles import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('create', views.create_user, name='create_user'),
    path('phone', views.add_mobile_number, name='add_mobile_number'),
]
