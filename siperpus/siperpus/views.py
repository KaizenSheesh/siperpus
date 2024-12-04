from django.shortcuts import render
import json
import os

BOOKS_FILE = os.path.join(os.path.dirname(__file__), '../books_api.')

def homepage(request):
    return render(request, 'home.html')
def books(request):
    return render(request, 'books.html')