from django.test import TestCase
from django.db.models import Avg

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
        authors = authors.annotate_annotated_book_count().all()
        author = authors[0]
        self.assertEqual(author.annotated_book_count, author.book_count())
        self.assertEqual(author.annotated_book_count, author.manual_book_count())

    def test_can_access_annotations(self):
        authors = Author.objects.filter(id=self.a1.id)
        aggregations = authors.annotate_annotated_book_count().aggregate(Avg('annotated_book_count'))
        self.assertIn('annotated_book_count__avg', aggregations)
        average_annotated_book_count = aggregations['annotated_book_count__avg']
        self.assertEqual(average_annotated_book_count, 5.0)
