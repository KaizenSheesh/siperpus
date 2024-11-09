from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from .session_auth import SessionAuth
from .decorators import role_required
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role') or 'user'  # Default role is 'user' if not provided
        
        # Register user using SessionAuth, which writes to accounts.json
        success, message = SessionAuth.register_user(username, password, role)
        
        if success:
            messages.success(request, 'Registrasi akun berhasil! Silahkan Login!')
            return redirect('login')
        else:
            messages.error(request, message)
            
    return render(request, 'auth/register.html')

@ensure_csrf_cookie
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user using SessionAuth, which reads from accounts.json
        if SessionAuth.login(request, username, password):
            messages.success(request, 'Login Berhasil')
            return redirect('home')
        else:
            messages.error(request, 'Username atau Password salah')
            
    return render(request, 'auth/login.html')

def logout_view(request):
    # Logout user by clearing session
    SessionAuth.logout(request)
    messages.info(request, 'Logout Berhasil!')
    return redirect('login')

def home_view(request):
    # Get current user from session and pass to template
    user = SessionAuth.get_current_user(request)
    return render(request, 'home.html', {'user': user})

def add_staff(request):
    # Cek apakah pengguna yang login adalah admin
    current_user = SessionAuth.get_current_user(request)
    if current_user is None or current_user['role'] != 'admin':
        return redirect('/login/')  # Jika bukan admin, redirect ke login
    
    # Jika form dikirimkan
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Register user dengan role 'staff'
        success, message = SessionAuth.register_user(username, password, role="staff")
        
        if not success:
            return render(request, 'admin/add_staff.html', {'error': message})
        
        return redirect('/')  # Redirect ke halaman admin setelah berhasil menambahkan staff

    # Jika GET request, tampilkan halaman form
    return render(request, 'admin/add_staff.html')