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

    book_count = djangotation.tations.count('book')
    book_count_book_count = djangotation.tations.sum('book_count', 'book_count')

    other_book_count = djangotation.tations.count('book', groups=['books'])
    # Author.objects.annotate_books()
    # Author.objects.annotate_group('books')
    # Author.objects.annotate_groups(['books'])

# Uber Future

class Book:
    
    page_count = djangotation.tations.count('page')

class Author:

    page_count = djangotation.tations.count('book__page_count')
    
    # Might need to be with a custom F() class :/
    @djangotation.annotation(Count('book__page_count'))
    def other_page_count(self):
        return operator.add(book.page_set.count() for book in author.book_set.all())
```
