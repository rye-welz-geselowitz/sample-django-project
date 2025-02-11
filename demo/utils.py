from datetime import date, datetime

from demo.models import Author, Book, Genre

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

def compare_runtimes_and_results(f1, f2, *args, **kwargs):
    def _get_results_and_runtime_ms(f):
        start_dt = datetime.now()
        res = f(*args, **kwargs)
        miliseconds = (datetime.now() - start_dt).total_seconds() * 1000 
        return (res, miliseconds)
    
    (f1_res, f1_ms) = _get_results_and_runtime_ms(f1)
    (f2_res, f2_ms) = _get_results_and_runtime_ms(f2)

    print(f'\nComparing {f1.__name__} and {f2.__name__}')
    print(f'Results were {"" if f1_res == f2_res else "NOT "}the same')
    if f1_res != f2_res:
        for (f, res) in [
            (f1, f1_res),
            (f2, f2_res),
        ]:
            print(f'{f.__name__} -  {str(res)[:100]}{"..." if len(str(res)) > 100 else ""}')
       

    [(faster, faster_ms), (slower, slower_ms)] = sorted(
        [(f1, f1_ms), (f2, f2_ms)],
        key=lambda x: x[1]
    )

    speed_comparison = 'infinitely' if faster_ms == 0 else f'{(slower_ms / faster_ms):.0f} times'

    print(f'{faster.__name__} was {speed_comparison} faster than {slower.__name__} '
          f'({faster_ms:.01f} milliseconds vs. {slower_ms:.01f} milliseconds)')

def maybe_populate():
    book_count = Book.objects.count()
    genre_count = Genre.objects.count()
    if book_count > 0 and genre_count > 0:
        return 
    
    print('Clearing database')
    Genre.objects.all().delete()
    Book.objects.all().delete()
    Author.objects.all().delete() 

    print('Populating database!')

    for genre_name in ['Sci fi', 'Fantasy', 'Horror', 'Lit Fic']:
        genre = Genre(name=genre_name)
        genre.save()
    
    for (author_name, title, page_count, genre_names) in [
        ('JRR Tolkien', 'Return of the King', 504, ['Fantasy']),
        ('Chinua Achebe', 'Things Fall Apart', 301, ['Lit Fic']),
        ('Han Kang', 'The Vegetarian', 200, ['Lit Fic', 'Horror'])
    ]:
        genres = Genre.objects.filter(name__in=genre_names).all()
        author = Author(name=author_name)
        author.save()
        book = Book(title=title, title_without_index=title,
            page_count=page_count, author=author
        )
        book.save()
        book.genres.set(genres)
    
    # Add an author with multiple books
    author = Author(name='Author McAuthor')
    author.save()
    for (title, publication_date, page_count) in [
        ('Apple Book', date(2016, 5, 1), 100),
        ('Banana Book', date(2018, 10, 10), 200),
        ('Pear Book', date(2020, 12, 1), 155),
    ]:
        book = Book(title=title, title_without_index=title,
            page_count=page_count, author=author,
            publication_date=publication_date
        )
        book.save()

    for i in range(100_000):
        genres = Genre.objects.filter(name__in=['Lit Fic']).all()
        title = f'Book {i}'
        author = Author(name=f'Author {i}')
        author.save()
        book = Book(title=title,
            title_without_index=title,
            page_count=100,
            author=author
        )
        book.save()  
        book.genres.set(genres)
