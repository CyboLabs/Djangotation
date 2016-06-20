from django.test import TestCase

from .models import *


class TestStub(TestCase):

    def setUp(self):
        self.a1 = Author.objects.create()

        self.books = [
            Book.objects.create(author=self.a1),
            Book.objects.create(author=self.a1),
            Book.objects.create(author=self.a1),
            Book.objects.create(author=self.a1),
            Book.objects.create(author=self.a1)
        ]

    def test_stub(self):
        authors = Author.objects.filter(id=self.a1.id)
        import pdb; pdb.set_trace();
        pass
        authors = authors.annotate_annotated_book_count().all()
