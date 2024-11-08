from typing import Any
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_respone):
        self.get_respone = get_respone

    def __call__(self, request):
        address_url = [
            reverse('login'),
            reverse('register')
        ]

        if not request.session.get('current_user') and request.path not in address_url:
            return redirect('login')
        
        respone = self.get_respone(request)
        return respone