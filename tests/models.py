from django.db import models

from djangotation import Manager, annotation, tations


class Author(models.Model):
    objects = Manager()

    @annotation(models.Count('book'))
    def annotated_book_count(self):
        return self.book_set.count()

    def book_count(self):
        return self.book_set.count()

    def manual_book_count(self):
        return len(self.book_set.all())

    generic_book_count = tations.count('book')


class Book(models.Model):
    objects = Manager()

    author = models.ForeignKey(Author)
