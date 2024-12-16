from typing import Any
from django.shortcuts import redirect
from register.session_auth import SessionAuth
from django.urls import reverse
from django.http import HttpResponseForbidden

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
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        protected_urls = {
            '/daftar-permintaan/': 'staff',
        }

        if request.path in protected_urls:
            required_role = protected_urls[request.path]

            user = SessionAuth.get_current_user(request)

            if user is None or user['role'] != required_role:
                if user is None:
                    return redirect(reverse('login'))
                return HttpResponseForbidden('<h1>403 Forbidden</h1><p>Anda tidak memiliki akses ke halaman ini.</p>')

        return None
    