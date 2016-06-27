# Djangotation
Django Annotations extended framework

```python
# Now

class Author:

    @djangotation.annotation(Count('book'))
    def book_count(self):
        return self.book_set.count()
    
# Future

class Author:

    book_count = djangotation.tations.count('book', name='book_count')
    book_count_book_count = djangotation.tations.sum('book_count', 'book_count', name='book_count_book_count')

    other_book_count = djangotation.tations.count('book', name='other_book_count', groups=['books'])
    # Author.objects.annotate_books()
    # Author.objects.annotate_group('books')
    # Author.objects.annotate_groups(['books'])

# Uber Future

class Book:
    
    page_count = djangotation.tations.count('page', name='page_count')

class Author:

    page_count = djangotation.tations.count('book__page_count', name='page_count')
    
    @djangotation.annotation(Count('book__page_count'))
    def other_page_count(self):
        return operator.add(book.page_set.count() for book in author.book_set.all())
```
