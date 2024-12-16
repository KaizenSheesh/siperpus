import json
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from register.session_auth import SessionAuth
from django.views.decorators.csrf import ensure_csrf_cookie

BOOKS_FILE = os.path.join(os.path.dirname(__file__), 'data/books.json')
BORROWS_FILE = os.path.join(os.path.dirname(__file__), 'data/peminjaman.json')

def read_books_from_file(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as file:
        return json.load(file)

def write_books_to_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

@api_view(['GET'])
def get_books(request):
    books = read_books_from_file(BOOKS_FILE)
    return Response(books)

@api_view(['GET'])
def get_book(request, book_id):
    books = read_books_from_file(BOOKS_FILE)
    book = next((b for b in books if b['id'] == book_id), None)
    if book:
        return Response(book)
    return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['POST'])
def add_book(request):
    if request.method == 'POST':
        print("Data yang diterima:", request.data)
        noarsip = request.data.get('no_arsip')
        nama_mhs = request.data.get('nama_mhs')
        nim = request.data.get('nim')
        judul = request.data.get('judul')
        dospem = request.data.get('dospem')
        tahun_lulus = request.data.get('tahun_lulus')

        # Validasi data
        if not all([noarsip, nama_mhs, nim, judul, dospem, tahun_lulus]):
            return Response({'success': False, 'message': 'Incomplete data'}, status=400)
        
        try:
            # Konversi tahun_lulus menjadi integer
            tahun_lulus = int(tahun_lulus)
        except ValueError:
            return Response({'success': False, 'message': 'tahun_lulus harus berupa angka'}, status=400)

        new_book = {
            'id': max([b['id'] for b in read_books_from_file(BOOKS_FILE)], default=0) + 1,
            'no_arsip': noarsip,
            'nama_mhs': nama_mhs,
            'nim': nim,
            'judul': judul,
            'dospem': dospem,
            'tahun_lulus': tahun_lulus,  # Sudah berupa integer
            'status': "Tersedia"
        }

        books = read_books_from_file(BOOKS_FILE)
        books.append(new_book)
        write_books_to_file(BOOKS_FILE, books)
        
        return Response({'success': True, 'message': 'Book added successfully'}, status=201)

@api_view(['POST'])
@csrf_exempt 
def edit_book(request, book_id):
    books = read_books_from_file(BOOKS_FILE)
    book = next((b for b in books if b['id'] == book_id), None)

    if not book:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        try:
            data = request.data
            book['no_arsip'] = data['no_arsip']
            book['nama_mhs'] = data['nama_mhs']
            book['nim'] = data['nim']
            book['judul'] = data['judul']
            book['dospem'] = data['dospem']
            book['tahun_lulus'] = int(data['tahun_lulus'])
            book['status'] = data['status']
            
            write_books_to_file(BOOKS_FILE, books)
            return Response({'success': True}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'book': book}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_book(request, book_id):
    books = read_books_from_file(BOOKS_FILE)
    updated_books = [b for b in books if b['id'] != book_id]
    
    if len(updated_books) == len(books):
        return Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    
    write_books_to_file(BOOKS_FILE, updated_books)
    return Response({'detail': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_peminjaman(request):
    user = SessionAuth.get_current_user(request)  # Mendapatkan user yang sedang login
    filter_type = request.query_params.get('filter', 'all')  # Mendapatkan parameter filter dari request
    
    with open(BORROWS_FILE, 'r') as file:
        peminjaman_data = json.load(file)
    
    if filter_type == 'current':  # Filter untuk buku yang sedang dipinjam
        filtered_data = [
            item for item in peminjaman_data 
            if item["username"] == user["username"] and item["status"] == "approved"
        ]
    else:
        filtered_data = peminjaman_data
    
    return Response(filtered_data)
