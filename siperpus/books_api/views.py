import json
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt


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
@api_view(['POST'])
def add_book(request):
    if request.method == 'POST':
        print("Data yang diterima:", request.data)
        title = request.data.get('title')
        author = request.data.get('author')
        category = request.data.get('category')
        lok_rak = request.data.get('lok_rak')

        if not all([title, author, category, lok_rak]):
            return Response({'success': False, 'message': 'Incomplete data'}, status=400)

        new_book = {
            'title': title,
            'author': author,
            'category': category,
            'lok_rak': lok_rak,
            'id': max([b['id'] for b in read_books_from_file()], default=0) + 1
        }

        books = read_books_from_file()
        books.append(new_book)
        write_books_to_file(books)
        
        return Response({'success': True, 'message': 'Book added successfully'}, status=201)


@api_view(['POST'])
@csrf_exempt 
def edit_book(request, book_id):
    books = read_books_from_file()
    book = next((b for b in books if b['id'] == book_id), None)

    if not book:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        try:
            data = request.data
            book['title'] = data['title']
            book['author'] = data['author']
            book['category'] = data['category']
            book['lok_rak'] = data['lok_rak']
            
            write_books_to_file(books)
            return Response({'success': True}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'book': book}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_book(request, book_id):
    books = read_books_from_file()
    updated_books = [b for b in books if b['id'] != book_id]
    
    if len(updated_books) == len(books):
        return Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    
    write_books_to_file(updated_books)
    return Response({'detail': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
