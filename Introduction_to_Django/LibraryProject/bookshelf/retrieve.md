```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
# Expected Output: 1984 George Orwell 1949
```