

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import OuterRef, Subquery

from demo.models import Book
from demo.utils import compare_runtimes_and_results, maybe_populate

# select_related works by creating an SQL join and including the fields of the related object in
# the SELECT statement. For this reason, select_related gets the related objects in the same database
# query. However, to avoid the much larger result set that would result from joining across a ‘many’
# relationship, select_related is limited to single-valued relationships - foreign key and one-to-one.

# prefetch_related, on the other hand, does a separate lookup for each relationship, and does
# the ‘joining’ in Python. This allows it to prefetch many-to-many, many-to-one, and
# GenericRelation objects which cannot be done using select_related, in addition to the
# foreign key and one-to-one relationships that are supported by select_related.
# It also supports prefetching of GenericForeignKey, however, the queryset for each
# ContentType must be provided in the querysets parameter of GenericPrefetch.


# * Come up with a situation where writing raw SQL is easier than using the Django models
def get_list_of_titles_excluding_latest_books_by_author():
    """ Let's say there's a book prize that can only be given to 
    books that are NOT the author's latest work. Find a list of all 
    candidate books.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
                WITH latest_books as (
                    SELECT DISTINCT ON (author_id) demo_book.id as book_id
                    FROM demo_book
                    ORDER BY author_id, publication_date DESC
                )
                SELECT DISTINCT title
                FROM demo_book
                LEFT JOIN latest_books on latest_books.book_id = demo_book.id 
                ORDER BY title
            """
        )
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return [result['title'] for result in results]

def get_list_of_titles_excluding_latest_books_by_author_2():
    # Subquery to get the most recent book for each author
    latest_books = Book.objects.filter(
        author=OuterRef('pk')  # Reference to the author in the outer query
    ).order_by('-publication_date')  # Sort by publication date (most recent first)

    # Get all books except the latest ones per author
    candidate_books = Book.objects.exclude(
        id__in=Subquery(latest_books.values('id')[:1])  # Exclude the latest book for each author
    ).values_list('title', flat=True).distinct().order_by('title')  # Return distinct titles, ordered

    return list(candidate_books)

# * Come up with a situation where using prefetch_related is better than select_related 
# NOTE: I couldn't actually come up with a situation where select_related performance was worse
def get_book_genres_PREFETCH_RELATED(book_titles):
    records = Book.objects.prefetch_related('genres').values('genres__name').filter(title__in=book_titles).order_by('genres__name').all()
    return list(set([record['genres__name'] for record in records]))

def get_book_genres_SELECT_RELATED(book_titles):
    records = Book.objects.select_related('genres').values('genres__name').order_by('genres__name').filter(title__in=book_titles).all()
    return list(set([record['genres__name'] for record in records]))

# * Come up with a situation where select_related is better than prefetch_related
def get_books_with_author_info_SELECT_RELATED():
    books = Book.objects.select_related('author').order_by('title', 'author__name').all()
    return [
        f'{book.title} is by {book.author.name}' for book in books
    ]

def get_books_with_author_info_PREFETCH_RELATED():
    books = Book.objects.prefetch_related('author').order_by('title', 'author__name').all()
    return [
        f'{book.title} is by {book.author.name}' for book in books
    ]

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        maybe_populate()

        book_titles = [book['title'] for book in Book.objects.values('title').all()]

        # Hmmmm... performance is basically identical!
        compare_runtimes_and_results(
            get_book_genres_PREFETCH_RELATED,
            get_book_genres_SELECT_RELATED,
            book_titles
        )

        compare_runtimes_and_results(
            get_list_of_titles_excluding_latest_books_by_author,
            get_list_of_titles_excluding_latest_books_by_author_2
        )

        compare_runtimes_and_results(
            get_books_with_author_info_SELECT_RELATED,
            get_books_with_author_info_PREFETCH_RELATED
        )


        
        