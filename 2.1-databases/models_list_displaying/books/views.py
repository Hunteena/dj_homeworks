from django.shortcuts import render, redirect

from books.models import Book


def index(request):
    return redirect('books')


def _books_by_rows(all_books, row_length=3):
    return [
        all_books[i: i + row_length]
        for i in range(0, len(all_books), row_length)
    ]


def books_view(request):
    template = 'books/books_list.html'
    all_books = Book.objects.all()
    context = {'books': _books_by_rows(all_books)}
    return render(request, template, context)


def books_by_date_view(request, pub_date):
    template = 'books/books_list.html'
    all_books = Book.objects.filter(pub_date=pub_date)
    context = {'books': _books_by_rows(all_books)}

    query = Book.objects.filter(pub_date__gt=pub_date)
    if query:
        context['next'] = query.order_by('pub_date')[0]
    query = Book.objects.filter(pub_date__lt=pub_date)
    if query:
        context['previous'] = query.order_by('-pub_date')[0]
    return render(request, template, context)
