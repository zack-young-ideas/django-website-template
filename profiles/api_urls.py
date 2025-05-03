"""
Defines the URL used to validate a user's mobile number.
"""

from django.urls import path

from profiles import apis


urlpatterns = [
    path(
        'mobile/verify',
        apis.verify_mobile_number,
        name='verify_mobile_number'
    ),
]
