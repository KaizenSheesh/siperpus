from django.shortcuts import render

def homepage(request):
    return render(request, 'home.html')
def books(request):
    return render(request, 'books.html')
def peminjaman(request):
    return render(request, 'peminjaman.html')