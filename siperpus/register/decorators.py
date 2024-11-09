from django.http import JsonResponse
from .session_auth import SessionAuth

def role_required(required_role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            current_user = SessionAuth.get_current_user(request)
            if not current_user or current_user['role'] != required_role:
                return JsonResponse({'error': 'Unauthorized access'}, status=403)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
