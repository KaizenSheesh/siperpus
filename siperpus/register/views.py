from django.shortcuts import render, redirect
from django.contrib import messages
from .session_auth import SessionAuth
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        success, message = SessionAuth.register_user(request, username, password, role)
        
        if success:
            messages.success(request, 'Registrasi akun berhasil!, Silahkan Login!')
            return redirect('login')
        else:
            messages.error(request, message)
            
    return render(request, 'auth/register.html')

@ensure_csrf_cookie
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if SessionAuth.authenticate(request, username, password):
            messages.success(request, 'Login Berhasil')
            return redirect('home')
        else:
            messages.error(request, 'Username atau Password salah')
            
    return render(request, 'auth/login.html')

def logout_view(request):
    SessionAuth.logout(request)
    # messages.info(request, 'Logout Berhasil!.')
    return redirect('login')

def home_view(request):
    user = SessionAuth.get_current_user(request)
    return render(request, 'home.html', {'user': user})