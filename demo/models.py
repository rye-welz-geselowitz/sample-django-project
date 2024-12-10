from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    # NOTE: We have separate `title` and `title_without_index` fields
    # for educational purposes only. In real life we would only keep 
    # one of these fields
    title = models.CharField(max_length=255, db_index=True)
    title_without_index = models.CharField(max_length=255)

    page_count = models.IntegerField()
    publication_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title


