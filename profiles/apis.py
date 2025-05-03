"""
Defines API endpoints used by frontend scripts.
"""

import json

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse

from drivers import sms
from profiles import forms


@login_required
def verify_mobile_number(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = forms.MobileNumberForm(data)
        if form.is_valid():
            mobile_number = str(form.cleaned_data['mobile_number'])
            request.user.add_new_mobile_number(mobile_number)
            print(sms.messages[0].message)
            return HttpResponse(content_type='application/json')
        else:
            response = {
                'error': 'Please enter a valid phone number'
            }
            return HttpResponse(
                json.dumps(response),
                status=400,
                content_type='application/json'
            )
    raise Http404()
