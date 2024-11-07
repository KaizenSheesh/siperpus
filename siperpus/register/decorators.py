# decorators.py
from functools import wraps
from django.shortcuts import redirect
from .session_auth import SessionAuth

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not SessionAuth.get_current_user(request):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper