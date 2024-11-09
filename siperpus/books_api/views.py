import json
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

# books = [
#     {'id': 1, 'title': 'Sistem Informasi Perkebunan', 'author': 'John Doe', 'category': 'Sistem Informasi', 'lok_rak': '3B'},
#     {'id': 2, 'title': 'Dashboard Perusahaan PTPN', 'author': 'Jane Doe',  'category': 'Dashboard', 'lok_rak': '4D'},
# ]

BOOKS_FILE = os.path.join(os.path.dirname(__file__), 'books.json')

def read_books_from_file():
    with open(BOOKS_FILE, 'r') as file:
        return json.load(file)

def write_books_to_file(books):
    with open(BOOKS_FILE, 'w') as file:
        json.dump(books, file, indent=4)

@api_view(['GET'])
def get_books(request):
    books = read_books_from_file()
    return Response(books)

@api_view(['GET'])
def get_book(request, book_id):
    books = read_books_from_file()
    book = next((b for b in books if b['id'] == book_id), None)
    if book:
        return Response(book)
    return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

def add_book(request):
    if request.method == 'POST':
        new_book = {
            'title': request.POST['title'],
            'author': request.POST['author'],
            'category': request.POST['category'],
            'lok_rak': request.POST['lok_rak'],
            'id': max([b['id'] for b in read_books_from_file()], default=0) + 1
        }
        books = read_books_from_file()
        books.append(new_book)
        write_books_to_file(books)
        return redirect('/') 
    return render(request, 'api_books/add_book.html')

def edit_book(request, book_id):
    books = read_books_from_file()
    book = next((b for b in books if b['id'] == book_id), None)

    if not book:
        return redirect('/')

    if request.method == 'POST':
        book['title'] = request.POST['title']
        book['author'] = request.POST['author']
        book['category'] = request.POST['category']
        book['lok_rak'] = request.POST['lok_rak']
        
        write_books_to_file(books)
        
        return redirect('/')

    return render(request, 'api_books/edit_book.html', {'book': book})

@api_view(['DELETE'])
def delete_book(request, book_id):
    books = read_books_from_file()
    updated_books = [b for b in books if b['id'] != book_id]
    
    if len(updated_books) == len(books):
        return Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    
    write_books_to_file(updated_books)
    return Response({'detail': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
