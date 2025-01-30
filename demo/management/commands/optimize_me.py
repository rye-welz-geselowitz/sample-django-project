from datetime import datetime

from django.core.management.base import BaseCommand
from django.db.models import Count, F

from demo.models import Author, Book
from demo.utils import compare_runtimes_and_results, maybe_populate


def get_formatted_author_intros(author_ids):
    intros = []
    for author_id in  author_ids:
        author = Author.objects.get(id=author_id)
        books = Book.objects.filter(author_id=author_id).all()
        intros.append(
            f'{author.name} is known for writing {len(books)} book(s).'
        )
    return intros
    
def get_formatted_author_intros_OPTIMIZED(author_ids):
    intros = []
    authors = Author.objects.prefetch_related('books').filter(id__in=(author_ids))
    for author in authors:
        intros.append(
            f'{author.name} is known for writing {len(author.books.all())} book(s).'
        )
    return intros
    

def get_formatted_author_intros_OPTIMIZED_2(author_ids):
    intros = []
    authors = Author.objects.filter(id__in=author_ids).annotate(book_count=Count("books"))
    for author in authors:
        intros.append(
            f'{author.name} is known for writing {author.book_count} book(s).'
        )
    return intros

def get_highest_page_count_book_title():
    highest_page_count_seen = 0
    title_of_highest_page_count_seen = None 
    all_title_data = Book.objects.values('title')
    for title_data in all_title_data:
        title = title_data['title']
        book = Book.objects.filter(title = title).first()
        if book.page_count > highest_page_count_seen:
            highest_page_count_seen = book.page_count
            title_of_highest_page_count_seen = book.title  
    return title_of_highest_page_count_seen

def get_highest_page_count_book_title_OPTIMIZED():
    book = Book.objects.all().order_by('-page_count').first()
    return book.title

def get_book_intros(book_ids):
    intros = []
    for book_id in  book_ids:
        book = Book.objects.get(id=book_id)
        author = Author.objects.filter(id=book.author_id).first()
        intros.append(f'{book.title} is by {author.name} and has {book.page_count} pages')
    return intros

def get_book_intros_OPTIMIZED(book_ids):
    intros = []
    books = Book.objects.prefetch_related('author').filter(id__in=(book_ids))
    for book in  books:
        intros.append(f'{book.title} is by {book.author.name} and has {book.page_count} pages')
    return intros

def get_book_intros_OPTIMIZED_2(book_ids):
    intros = []
    books = Book.objects.filter(id__in=(book_ids)).annotate(author_name=F("author__name")).order_by("id")
    for book in  books:
        intros.append(f'{book.title} is by {book.author_name} and has {book.page_count} pages')
    return intros

class Command(BaseCommand):
    help = 'Runs a custom demo command'

    def handle(self, *args, **kwargs):
        maybe_populate()

        author_ids = list(range(1, 50_000))
        compare_runtimes_and_results(
            get_formatted_author_intros,
            get_formatted_author_intros_OPTIMIZED,
            author_ids
        )

        compare_runtimes_and_results(
            get_formatted_author_intros,
            get_formatted_author_intros_OPTIMIZED_2,
            author_ids
        )

        compare_runtimes_and_results(
            get_highest_page_count_book_title,
            get_highest_page_count_book_title_OPTIMIZED,
        )

        book_ids = list(range(3, 51_000))
        compare_runtimes_and_results(
            get_book_intros,
            get_book_intros_OPTIMIZED,
            book_ids
        )

        compare_runtimes_and_results(
            get_book_intros,
            get_book_intros_OPTIMIZED_2,
            book_ids
        )