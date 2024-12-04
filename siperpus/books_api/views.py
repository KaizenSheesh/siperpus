import json
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.shortcuts import render, redirect

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

def borrow_book(request):
    if request.method == 'POST':
        book_id = int(request.POST['book_id'])
        borrow_date = request.POST['borrow_date']
        return_date = request.POST['return_date']

        books = read_books_from_file()
        borrowed_books = read_borrows_from_file()
        
        # Cari buku yang akan dipinjam
        book = next((b for b in books if b['id'] == book_id), None)

        if book and not book.get('is_borrowed', False):
            # Update status buku di file buku utama
            book['is_borrowed'] = True
            write_books_to_file(books)

            # Tambahkan data ke borrowed_books.json
            borrowed_books.append({
                "book_id": book_id,
                "borrower": request.user.username,
                "borrow_date": borrow_date,
                "return_date": return_date
            })
            write_borrows_to_file(borrowed_books)
            
            return redirect('/')
        else:
            return render(request, 'api_books/borrow_book.html', {'error': 'Buku tidak tersedia untuk dipinjam'})
    else:
        # Hanya tampilkan buku yang tersedia untuk dipinjam
        books = [b for b in read_books_from_file() if not b.get('is_borrowed', False)]
        return render(request, 'api_books/borrow_book.html', {'books': books})

def return_book(request):
    if request.method == 'POST':
        book_id = int(request.POST['book_id'])

        books = read_books_from_file()
        borrowed_books = read_borrows_from_file()
        
        # Cari buku yang akan dikembalikan
        book = next((b for b in books if b['id'] == book_id), None)
        borrowed_book = next((b for b in borrowed_books if b['book_id'] == book_id and b['borrower'] == request.user.username), None)

        if book and book.get('is_borrowed', False) and borrowed_book:
            # Update status buku
            book['is_borrowed'] = False
            write_books_to_file(books)

            # Hapus data dari borrowed_books.json
            borrowed_books = [b for b in borrowed_books if not (b['book_id'] == book_id and b['borrower'] == request.user.username)]
            write_borrows_to_file(borrowed_books)

            return redirect('/')
        else:
            return render(request, 'api_books/return_book.html', {'error': 'Buku tidak ditemukan atau sudah dikembalikan'})
    else:
        # Tampilkan buku yang dipinjam oleh user yang login
        borrowed_books = read_borrows_from_file()
        user_borrowed_books = [b for b in borrowed_books if b['borrower'] == request.user.username]
        return render(request, 'api_books/return_book.html', {'borrowed_books': user_borrowed_books})
