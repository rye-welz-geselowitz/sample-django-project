from datetime import datetime

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
