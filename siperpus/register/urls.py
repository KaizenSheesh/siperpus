from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/add_staff/', views.add_staff, name='add_staff'),
    path('', views.home_view, name='home'),
    path('books/', views.books_view, name='books'),
]