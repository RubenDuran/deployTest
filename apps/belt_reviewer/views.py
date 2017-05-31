from django.shortcuts import render, redirect
from django.contrib import messages
from . models import User, Author, Review, Book
from django.db.models import Count

# Create your views here.
def index(request):
    return render(request,'belt_reviewer/index.html')

def add_books(request):
    return render(request, 'belt_reviewer/add_books.html')

def add(request):
    if request.method == 'POST':
        errors = Book.objects.validate(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            if request.POST['new_author'] != "":
                author = request.POST['new_author']
            else:
                author = request.POST['author']

            try:
                author_id = Author.objects.get(name=author)
            except:
                author_id = Author.objects.create(name=author, created_at='NOW()', updated_at='NOW()')

            user = User.objects.get(pk = request.session['user_id'])

            messages.success(request, 'Successfully Added book')

            new_book = Book.objects.create(title=request.POST['title'], genre='self-help', author= author_id, rating=request.POST['rating'], created_at='NOW()', updated_at='NOW()')

            Review.objects.create(user=user, book=new_book, content= request.POST['review'], created_at='NOW()', updated_at='NOW()')
            return redirect('/books/{}'.format(new_book.id))
    return redirect('/books')

def book(request, id):
    book_id = id
    book = Book.objects.get(pk = book_id)
    review = Review.objects.get(book = book.id)

    context = {
        'book': book,
        'review': review,
    }
    return render(request, 'belt_reviewer/book.html', context)

def books(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')
    user = User.objects.get(pk=user_id)
    books = Book.objects.all()
    reviews = Review.objects.all().order_by('-created_at')

    context = {
        'user': user,
        'books': books,
        'reviews': reviews,
        }
    return render(request, 'belt_reviewer/books.html',context)

def register(request):
    if request.method == 'POST':
        errors = User.objects.validate(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            messages.success(request, 'Successfully registered!')
            User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST[
                                'email'], password=request.POST['pw'], created_at='NOW()', updated_at='NOW()')
            email=request.POST["email"]
            user_details = User.objects.filter(email=email)
            user = user_details[0]
            request.session['user_id'] = user.id
            return redirect('/books')
    return redirect('/')


def login(request):
    if request.method == 'POST':
        errors = User.objects.signin(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            messages.success(request, 'Successfully logged in!')
            email=request.POST["email"]
            user_details = User.objects.filter(email=email)
            user = user_details[0]
            request.session['user_id'] = user.id
            return redirect('/books')
        return redirect('/')

def logout(request):
    del request.session['user_id']
    return redirect('/')


def users(request, id):
    user_id = id
    user = User.objects.get(pk = user_id)
    review = Review.objects.filter(user = user.id)


    context = {
        'user': user,
        'review': review,
    }

    return render(request, 'belt_reviewer/user.html', context)
