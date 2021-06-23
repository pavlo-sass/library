from django.shortcuts import render, redirect
from django.http import HttpResponse

from authentication.models import CustomUser
from .forms import AddForm
from .models import Book


menu = [1, 2, 3]

BASE_CONREXT = {'menu': menu}

def index(request):
    list_books = list(Book.objects.all())
    answ = []
    for book in list_books:
        answ.append(Book.to_dict(book))
    context = {
        'list_books': answ,
        'title': 'Наші Книжки'
               }
    context.update(BASE_CONREXT)
    return render(request, 'book/index.html', context)

def create_book(request):
    if request.method == 'POST':
        form = AddForm(request.POST, request.FILES)
        if form.is_valid():
            try:

                Book.create(**form.cleaned_data)
                return redirect('books')
            except:
                form.add_error(None, 'При додавані книги виникла помилка')

    else:
        form = AddForm()
    context = {
        'title': "Створюємо нову книгу",
        'form': form
    }
    context.update(BASE_CONREXT)
    return render(request, 'book/addbook.html', context)

def get_book(request, book_id):
    book = Book.get_by_id(book_id)
    info = Book.to_dict(book)
    users = []
    users_list = book.order_set.all().values_list()
    for user in users_list:
        users.append(CustomUser.get_by_id(user[1]))
    context = {
        'title': f"{info['name']}",
        'info': info,
        'users': users
    }
    context.update(BASE_CONREXT)
    return render(request, 'book/user.html', context)

#TODO update authors
def update_book(request, book_id):
    book = Book.get_by_id(book_id)
    book_dict = Book.to_dict(book)
    form = AddForm(book_dict)
    if request.method == 'POST':
        form = AddForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                book.update(**form.cleaned_data)
                return redirect('books')
            except:
                form.add_error(None, 'При редагувані книжки виникла помилка')

    context = {
        'book_id': book_id,
        'title': "Редагуємо книжку",
        'form': form
    }
    context.update(BASE_CONREXT)
    return render(request, 'book/update_book.html', context)

def delete_book(request, book_id):
    if Book.delete_by_id(book_id):
        return redirect('books')
    return HttpResponse('Памілка!!!')