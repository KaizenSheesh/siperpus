import json
import os
import pandas as pd
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.http import JsonResponse
from register.session_auth import SessionAuth
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

BOOKS_FILE = os.path.join(os.path.dirname(__file__), "../books_api/data/books.json")
PEMINJAMAN_FILE = os.path.join(os.path.dirname(__file__), "../books_api/data/peminjaman.json")
ACCOUNTS_FILE = os.path.join(os.path.dirname(__file__), "../data/accounts.json")

notifications = [
    {"type": "success", "message": "Buku berhasil dikembalikan", "description": "Harap pinjam buku lain sesuai kebutuhan."},
    {"type": "warning", "message": "Batas waktu hampir habis", "description": "Buku 'Python Basics' harus dikembalikan besok."},
    {"type": "error", "message": "Buku telah melewati batas waktu", "description": "Harap segera kembalikan buku untuk menghindari denda."}
    ]

# Helper Functions
def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def read_books():
    with open(BOOKS_FILE, 'r') as file:
        return json.load(file)

def read_peminjaman():
    with open(PEMINJAMAN_FILE, 'r') as file:
        return json.load(file)

def write_peminjaman(data):
    with open(PEMINJAMAN_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def update_book_status(book_id, new_status):
    with open(BOOKS_FILE, 'r') as file:
        books_data = json.load(file)

    for buku in books_data:
        if buku["id"] == book_id:
            buku["status"] = new_status
            break

    with open(BOOKS_FILE, 'w') as file:
        json.dump(books_data, file, indent=4)
        
def export_books_and_peminjaman_to_xlsx(request):
    books_data = load_json_data(BOOKS_FILE)
    peminjaman_data = load_json_data(PEMINJAMAN_FILE)

    books_df = pd.DataFrame(books_data)
    peminjaman_df = pd.DataFrame(peminjaman_data)

    excel_file_path = os.path.join(os.path.dirname(__file__), "../books_api/data/daftar_buku.xlsx")
    with pd.ExcelWriter(excel_file_path, engine="xlsxwriter") as writer:
        books_df.to_excel(writer, sheet_name="Books", index=False)
        peminjaman_df.to_excel(writer, sheet_name="Peminjaman", index=False)

    with open(excel_file_path, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="daftar_buku.xlsx"'
        return response
        
def export_peminjaman_to_xlsx(request):
    peminjaman_data = load_json_data(PEMINJAMAN_FILE)
    peminjaman_df = pd.DataFrame(peminjaman_data)

    excel_file_path = os.path.join(os.path.dirname(__file__), "../books_api/data/peminjaman_data.xlsx")
    with pd.ExcelWriter(excel_file_path, engine="xlsxwriter") as writer:
        peminjaman_df.to_excel(writer, sheet_name="Peminjaman", index=False)

    with open(excel_file_path, 'rb') as excel_file:
        response = HttpResponse(
            excel_file.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="peminjaman_data.xlsx"'
        return response

@api_view(['GET'])
def get_books_peminjaman(request):
    books = read_books()
    return Response(books)
    
def update_book_status(book_id, new_status):
    with open(BOOKS_FILE, 'r') as file:
        books_data = json.load(file)

    for buku in books_data:
        if buku["id"] == book_id:
            buku["status"] = new_status
            break

    with open(BOOKS_FILE, 'w') as file:
        json.dump(books_data, file, indent=4)
        
@ensure_csrf_cookie
def home_view(request):
    user = SessionAuth.get_current_user(request)
    books = read_books()

    ta_count = len([book for book in books])
    ta_2023_count = len([book for book in books if book['tahun_lulus'] == 2023])
    ta_2024_count = len([book for book in books if book['tahun_lulus'] == 2024])

    peminjaman_data = load_json_data(PEMINJAMAN_FILE)
    today = datetime.now().date()

    notifications = get_notifications(peminjaman_data, user["username"], today)
    notification_count = len(notifications)

    return render(request, 'home.html', {
        'user': user,
        'ta_count': ta_count,
        'ta_2023_count': ta_2023_count,
        'ta_2024_count': ta_2024_count,
        'notifications': notifications,
        'notification_count': notification_count,
    })

@ensure_csrf_cookie
def books_view(request):
    user = SessionAuth.get_current_user(request)
    peminjaman_data = load_json_data(PEMINJAMAN_FILE)
    today = datetime.now().date()

    notifications = get_notifications(peminjaman_data, user["username"], today)
    notification_count = len(notifications)
    return render(request, 'books.html', {
        'user': user,
        'notifications': notifications,
        'notification_count': notification_count,
        })

def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def enrich_peminjaman_data(peminjaman_data, books_data):
    for item in peminjaman_data:
        book = next((b for b in books_data if b["id"] == item.get("book_id")), None)
        if book:
            item["judul"] = book.get("judul", "Tidak diketahui")
            item["no_arsip"] = book.get("no_arsip", "-")
        else:
            item["judul"] = "Buku tidak ditemukan"
            item["no_arsip"] = "-"
    return peminjaman_data

def get_notifications(peminjaman_data, username, today):
    notifications = []
    for item in peminjaman_data:
        if item.get("username") == username and item.get("status") == "Diterima":
            tgl_pengembalian = datetime.strptime(item.get("tgl_pengembalian"), "%Y-%m-%d").date()
            days_left = (tgl_pengembalian - today).days

            judul_buku = item.get('judul', 'Buku tidak ditemukan')

            if days_left <= 1:
                notifications.append({
                    "type": "warning",
                    "message": f"Kamu memiliki buku yang harus dikembalikan dalam {days_left} hari.",
                    "description": "Pastikan untuk mengembalikannya tepat waktu."
                })
            elif days_left < 0:
                notifications.append({
                    "type": "error",
                    "message": f"Kamu memiliki buku yang telah melewati tenggat waktu pengembalian.",
                    "description": "Segera kembalikan untuk menghindari denda."
                })
    return notifications

@ensure_csrf_cookie
def peminjaman_view(request):
    user = SessionAuth.get_current_user(request)
    username = user["username"]

    peminjaman_data = load_json_data(PEMINJAMAN_FILE)
    books_data = load_json_data(BOOKS_FILE)
    accounts_data = load_json_data(ACCOUNTS_FILE)

    user_account = next((acc for acc in accounts_data if acc.get("username") == username), None)

    peminjaman_data = enrich_peminjaman_data(peminjaman_data, books_data)

    today = datetime.now().date()
    books_dipinjam = [item for item in peminjaman_data if item.get("username") == username and item.get("status") == "Diterima"]
    riwayat = [item for item in peminjaman_data if item.get("username") == username]

    notifications = get_notifications(peminjaman_data, username, today)
    notification_count = len(notifications)

    return render(request, 'peminjaman.html', {
        'user': user,
        'riwayat': riwayat,
        'books_dipinjam': books_dipinjam,
        'notifications': notifications,
        'notification_count': notification_count,
        'user_account': user_account,
    })

@ensure_csrf_cookie
def daftar_permintaan(request):
    user = SessionAuth.get_current_user(request)

    with open(PEMINJAMAN_FILE, 'r') as file:
        peminjaman_data = json.load(file)

    with open(BOOKS_FILE, 'r') as file:
        books_data = json.load(file)
        
        peminjaman_data = load_json_data(PEMINJAMAN_FILE)
    today = datetime.now().date()

    notifications = get_notifications(peminjaman_data, user["username"], today)
    notification_count = len(notifications)
    
    pending_requests = []
    for req in peminjaman_data:
        if req["status"] == "pending":
            book = next((b for b in books_data if b["id"] == req["book_id"]), None)

            if book:
                req["no_arsip"] = book["no_arsip"]
                req["judul"] = book["judul"]
                req["tahun_lulus"] = book["tahun_lulus"]
            else:
                req["no_arsip"] = book["no_arsip"]
                req["judul"] = "Buku tidak ditemukan"
                req["tahun_lulus"] = "-"
            
            pending_requests.append(req)

    return render(request, 'daftar_permintaan.html', {
        'user': user,
        'pending_requests': pending_requests,
        'notifications': notifications,
        'notification_count': notification_count,
    })

def konfirmasi_peminjaman_view(request):
    user = SessionAuth.get_current_user(request)
    if request.method == "POST":
        peminjaman_id = request.POST.get("id")
        book_id = request.POST.get('bookId')
        with open(PEMINJAMAN_FILE, 'r') as file:
            peminjaman_data = json.load(file)
        with open(BOOKS_FILE, 'r') as file:
            book = json.load(file)
            
        peminjaman_data = load_json_data(PEMINJAMAN_FILE)
        today = datetime.now().date()

        notifications = get_notifications(peminjaman_data, user["username"], today)
        notification_count = len(notifications)
        
        peminjaman = next((req for req in peminjaman_data if req["id"] == int(peminjaman_id)), None)
        books = next((req for req in book if req["id"] == int(book_id)), None)

        if peminjaman:
            peminjaman["status"] = "Diterima"
            books["status"] = "Dipinjam"

            with open(PEMINJAMAN_FILE, 'w') as file:
                json.dump(peminjaman_data, file, indent=4)
                
            with open(BOOKS_FILE, 'w') as file:
                json.dump(book, file, indent=4)

            return redirect('/daftar-permintaan/', {
                'notifications': notifications, 
                'notification_count': notification_count,
                })
    return JsonResponse({"error": "Invalid Request"}, status=400)

@ensure_csrf_cookie
def peminjaman_buku_view(request):
    user = SessionAuth.get_current_user(request)
    with open(BOOKS_FILE, 'r') as file:
        data = json.load(file)
    
    with open(PEMINJAMAN_FILE, 'r') as file:
        peminjaman_data = json.load(file)

    book_id = request.GET.get('bookId')
    username = request.GET.get('username')

    try:
        book_id = int(book_id)
    except (ValueError, TypeError):
        book_id = None

    peminjaman_data = load_json_data(PEMINJAMAN_FILE)
    today = datetime.now().date()

    notifications = get_notifications(peminjaman_data, user["username"], today)
    
    buku_ditemukan = None
    if book_id is not None:
        buku_ditemukan = next((buku for buku in data if buku['id'] == book_id), None)

    if request.method == "POST":
        tgl_peminjaman = request.POST.get('tgl_peminjaman')
        tgl_pengembalian = request.POST.get('tgl_pengembalian')

        if buku_ditemukan:
            
            update_book_status(book_id, "Pending")
            
            new_peminjaman = {
                "id": len(peminjaman_data) + 1,
                "username": username,
                "book_id": book_id,
                "tgl_peminjaman": tgl_peminjaman,
                "tgl_pengembalian": tgl_pengembalian,
                "status": "pending"
            }
            peminjaman_data.append(new_peminjaman)

            with open(PEMINJAMAN_FILE, 'w') as file:
                json.dump(peminjaman_data, file, indent=4)

            messages.success(request, f"Peminjaman buku berhasil diajukan. Menunggu konfirmasi staff.")
        else:
            messages.error(request, "Buku tidak ditemukan.")

    context = {
        "user": user,
        "username": username,
        'notifications': notifications,
        "judul_buku": buku_ditemukan['judul'] if buku_ditemukan else "Buku tidak ditemukan",
    }
    return render(request, 'peminjaman_buku.html', context)

def pengembalian_buku(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        with open(PEMINJAMAN_FILE, 'r') as file:
            peminjaman_data = json.load(file)
        with open(BOOKS_FILE, 'r') as file:
            books_data = json.load(file)

        for item in peminjaman_data:
            if item["book_id"] == int(book_id) and item["status"] == "Diterima":
                item["status"] = "Sudah Dikembalikan"
                item["tanggal_pengembalian"] = datetime.now().strftime("%Y-%m-%d")

        for book in books_data:
            if book["id"] == int(book_id):
                book["status"] = "Tersedia"

        with open(PEMINJAMAN_FILE, 'w') as file:
            json.dump(peminjaman_data, file, indent=4)
        with open(BOOKS_FILE, 'w') as file:
            json.dump(books_data, file, indent=4)

        return redirect('/peminjaman')

    return JsonResponse({"error": "Invalid Request"}, status=400)