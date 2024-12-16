"""
URL configuration for siperpus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('books_api.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', views.home_view, name='home'),
    path('books/', views.books_view, name='books'),
    path('peminjaman/', views.peminjaman_view, name='peminjaman'),
    path('', include('register.urls')),
    path('peminjaman/buku/', views.peminjaman_buku_view, name='peminjaman_buku'),
    path('daftar-permintaan/', views.daftar_permintaan, name='daftar_permintaan'),
    path('konfirmasi-peminjaman/', views.konfirmasi_peminjaman_view, name='konfirmasi-peminjaman'),
    path('pengembalian-buku/', views.pengembalian_buku, name='pengembalian-buku'),
]