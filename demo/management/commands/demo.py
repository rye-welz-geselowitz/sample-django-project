from datetime import datetime

from django.core.management.base import BaseCommand

from demo.models import Author, Book

# UTILITY FUNCTIONS

def compare_function_runtimes(f1, f2, *args, **kwargs):
    def get_milliseconds(f):
        start_dt = datetime.now()
        f(*args, **kwargs)
        return  (datetime.now() - start_dt).total_seconds() * 1000 
    
    f1_milliseconds = get_milliseconds(f1)
    f2_milliseconds = get_milliseconds(f2)

    [(faster, faster_ms), (slower, slower_ms)] = sorted(
        [(f1, f1_milliseconds), (f2, f2_milliseconds)],
        key=lambda x: x[1]
    )

    print(f'{faster.__name__} was {(slower_ms / faster_ms):.0f} times faster than {slower.__name__} '
          f'({faster_ms:.01f} milliseconds vs. {slower_ms:.01f} milliseconds)')


def maybe_populate():
    book_count = Book.objects.count()
    if book_count > 0:
        return 
    
    print('Populating database!')
    
    for (author_name, title, page_count) in [
        ('JRR Tolkien', 'Return of the King', 504),
        ('Chinua Achebe', 'Things Fall Apart', 301),
        ('Han Kang', 'The Vegetarian', 200)
    ]:
        author = Author(name=author_name)
        author.save()
        book = Book(title=title, title_without_index=title, page_count=page_count, author=author)
        book.save()


    for i in range(100_000):
        title = f'Book {i}'
        author = Author(name=f'Author {i}')
        author.save()
        book = Book(title=title, title_without_index=title, page_count=100, author=author)
        book.save()  

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
