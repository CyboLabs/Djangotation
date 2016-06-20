from django.db import models

from djangotation import Manager, annotation


class Author(models.Model):
    objects = Manager()

    @annotation(models.Count('book'))
    def annotated_book_count(self):
        return self.book_set.count()

    def book_count(self):
        return self.book_set.count()

    def manual_book_count(self):
        return len(self.book_set.all())


class Book(models.Model):
    objects = Manager()

    author = models.ForeignKey(Author)
