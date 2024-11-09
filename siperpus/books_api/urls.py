from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.get_books, name='get_books'),
    path('books/<int:book_id>/', views.get_book, name='get_book'),
    path('add-book/', views.add_book, name='add_book'),
    path('books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
]
