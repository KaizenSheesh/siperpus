import json
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

BOOKS_FILE = os.path.join(os.path.dirname(__file__), 'books.json')
BORROWS_FILE = os.path.join(os.path.dirname(__file__), 'peminjaman.json')

def read_books_from_file():
    with open(BOOKS_FILE, 'r') as file:
        return json.load(file)

def write_books_to_file(books):
    with open(BOOKS_FILE, 'w') as file:
        json.dump(books, file, indent=4)

def read_borrows_from_file():
    with open(BORROWS_FILE, 'r') as file:
        return json.load(file)

def write_borrows_to_file(borrows):
    with open(BORROWS_FILE, 'w') as file:
        json.dump(borrows, file, indent=4)

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
        noarsip = request.data.get('noarsip')
        nama_mhs = request.data.get('nama_mhs')
        nim = request.data.get('nim')
        judul = request.data.get('judul')
        dospem = request.data.get('dospem')
        tahun_lulus = request.data.get('tahun_lulus')

        if not all([noarsip, nama_mhs, nim, judul, dospem, tahun_lulus]):
            return Response({'success': False, 'message': 'Incomplete data'}, status=400)

        new_book = {
            'noarsip': noarsip,
            'nama_mhs': nama_mhs,
            'nim': nim,
            'judul': judul,
            'dospem': dospem,
            'tahun_lulus': tahun_lulus,
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
            book['noarsip'] = data['noarsip']
            book['nama_mhs'] = data['nama_mhs']
            book['nim'] = data['nim']
            book['judul'] = data['judul']
            book['dospem'] = data['dospem']
            book['tahun_lulus'] = data['tahun_lulus']
            
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

@api_view(['POST'])
def peminjaman_buku(request, book_id):
    books = read_books_from_file()
    book = next((b for b in books if b['id'] == book_id), None)
    
    if not book:
        return Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    if book['is_borrowed']:
        return Response({'detail': 'Book is already borrowed'}, status=status.HTTP_400_BAD_REQUEST)

    book['is_borrowed'] = True
    borrows = read_borrows_from_file()
    new_borrow = {
        'user_id': request.data.get('user_id'),
        'book_id': book_id,
        'borrow_date': "2024-12-02T14:07:00Z",
        'return_date': "2024-12-09T14:07:00Z",
        'is_returned': False
    }
    borrows.append(new_borrow)

    write_books_to_file(books)
    write_borrows_to_file(borrows)

    return Response({'detail': 'Book borrowed successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def pengembalian_buku(request, book_id):
    books = read_books_from_file()
    book = next((b for b in books if b['id'] == book_id), None)

    if not book:
        return Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    if not book['is_borrowed']:
        return Response({'detail': 'Book is not borrowed'}, status=status.HTTP_400_BAD_REQUEST)

    book['is_borrowed'] = False
    borrows = read_borrows_from_file()
    borrow = next((b for b in borrows if b['book_id'] == book_id and not b['is_returned']), None)

    if borrow:
        borrow['is_returned'] = True

    write_books_to_file(books)
    write_borrows_to_file(borrows)

    return Response({'detail': 'Book returned successfully'}, status=status.HTTP_200_OK)