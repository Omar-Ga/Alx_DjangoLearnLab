from django.db import models

# Create your models here.

class Author(models.Model):
    """
    The Author model represents a writer of books.
    It contains the author's name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    The Book model represents a book written by an author.
    It contains the title, publication year, and a foreign key to the Author model.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
