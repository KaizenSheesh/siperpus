from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .session_auth import SessionAuth
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

@ensure_csrf_cookie
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role') or 'user'
        
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
    user = SessionAuth.get_current_user(request)
    return render(request, 'home.html', {'user': user})

@api_view(['POST'])
def add_staff(request):
    current_user = SessionAuth.get_current_user(request)
    if current_user is None or current_user['role'] != 'admin':
        return Response({'success': False, 'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return Response({'success': False, 'message': 'Username and Password are required.'}, status=status.HTTP_400_BAD_REQUEST)

            success, message = SessionAuth.register_user(username, password, role="staff")
            
            if not success:
                return Response({'success': False, 'message': message}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'success': True, 'message': 'Staff account added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)