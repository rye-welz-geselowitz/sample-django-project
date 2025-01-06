

from django.core.management.base import BaseCommand

from demo.models import Author, Book
from demo.utils import compare_function_runtimes, maybe_populate


##########################################
# FUNCTIONS TO TIME
##########################################
def get_books_by_title(titles):
   books = []
   for title in titles:
       book = Book.objects.filter(title=title).first()
       if book:
           books.append(book)
   return books

def get_books_by_title_bulk(titles):
   books = Book.objects.filter(title__in=titles)
   return books


##########################################
def count_books_by_author_db(author_id):
    return Book.objects.filter(author_id=author_id).count()

def count_books_by_author(author_id):
    author = Author.objects.get(id=author_id)
    return len(author.books.all())

##########################################
def get_book_by_title(title):
   book = Book.objects.filter(title=title).first()
   return book

def get_book_by_title_without_index(title):
   book = Book.objects.filter(title_without_index=title).first()
   return book
##########################################

def get_books_with_author_names():
    books = Book.objects.all()  # Retrieves all books
    result = []
    for book in books:
        result.append((book.title, book.author.name)) 
    return result


def get_books_with_author_names_select_related():
    books = Book.objects.select_related('author')
    return [(book.title, book.author.name) for book in books]

class Command(BaseCommand):
    help = 'Runs a custom demo command'

    def handle(self, *args, **kwargs):
        maybe_populate()

        print('\n\nFetching small number of titles')
        compare_function_runtimes(
            get_books_by_title_bulk,
            get_books_by_title,
            ['Things Fall Apart', 'The Vegetarian']
        )



        print('\n\nFetching large number of titles')
        compare_function_runtimes(
            get_books_by_title_bulk,
            get_books_by_title,
            [f'Book {i}' for i in range(5000)]
        )


        print('\n\nFetching single book')
        compare_function_runtimes(
            get_book_by_title,
            get_book_by_title_without_index,
            'Book 5001'
        )

        print('\n\nCounting books by author')
        compare_function_runtimes(
            count_books_by_author,
            count_books_by_author_db,
            2
        )

        print('\n\nGetting books with author names')
        compare_function_runtimes(
            get_books_with_author_names,
            get_books_with_author_names_select_related
        )
