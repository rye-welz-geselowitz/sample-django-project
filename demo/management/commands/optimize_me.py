from datetime import datetime
from django.db.models import Count,Max

from django.core.management.base import BaseCommand

from demo.models import Author, Book
from demo.utils import compare_runtimes_and_results, maybe_populate


def get_formatted_author_intros(author_ids):
    intros = []
    for author_id in  author_ids:
        author = Author.objects.get(id=author_id)
        books = Book.objects.filter(author_id=author_id).all()
        intros.append(
            f'{author.name} is known for writing {len(books)} book(s).' #annotate book count
        )
    return intros
    
def get_formatted_author_intros_OPTIMIZED(author_ids):
    # TODO: 
    # annotate the count of books! 
    authors = Author.objects.filter(id__in=author_ids).annotate(book_count=Count("books"))
    intros = [
            f'{author.name} is known for writing {author.book_count} book(s).'
            for author in authors
    ]
    return intros

def get_highest_page_count_book_title():
    highest_page_count_seen = 0 #aggregate using Max 
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
    # TODO use Max to get the highest page count then extract the title(2156 times faster) or just sort the page count in descending order(2707 times faster)

    # max_page_count = Book.objects.aggregate(max_page=Max('page_count'))['max_page']

    # book_with_max_page_count = Book.objects.filter(page_count=max_page_count).first()

    # return book_with_max_page_count.title if book_with_max_page_count else None
    
    highest_page_count_book = Book.objects.order_by('-page_count').first()

    return highest_page_count_book.title if highest_page_count_book else None

def get_book_intros(book_ids):
    intros = []
    for book_id in book_ids: 
        book = Book.objects.get(id=book_id) 
        author = Author.objects.filter(id=book.author_id).first()
        intros.append(f'{book.title} is by {author.name} and has {book.page_count} pages') 
    return intros

def get_book_intros_OPTIMIZED(book_ids):
    # TODO: optimize (prefetch related or select related)
    books = Book.objects.filter(id__in=book_ids).select_related('author')
    intros = [
        f'{book.title} is by {book.author.name} and has {book.page_count} pages'
        for book in books
    ]
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
            get_highest_page_count_book_title,
            get_highest_page_count_book_title_OPTIMIZED,
        )

        book_ids = list(range(3, 51_000))
        compare_runtimes_and_results(
            get_book_intros,
            get_book_intros_OPTIMIZED,
            book_ids
        )
