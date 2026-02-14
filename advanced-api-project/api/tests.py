from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book, Author
from django.urls import reverse

class BookAPITests(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create an author
        self.author = Author.objects.create(name="J.R.R. Tolkien")
        
        # Create a book
        self.book = Book.objects.create(
            title="The Hobbit",
            publication_year=1937,
            author=self.author
        )
        
        # URLs
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', args=[self.book.id])
        self.create_url = reverse('book-create')
        self.update_url = reverse('book-update', args=[self.book.id])
        self.delete_url = reverse('book-delete', args=[self.book.id])

    def test_list_books_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_detail_book_unauthenticated(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "The Hobbit")

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='password')
        data = {
            "title": "The Lord of the Rings",
            "publication_year": 1954,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_unauthenticated(self):
        data = {
            "title": "The Silmarillion",
            "publication_year": 1977,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # Or 401

    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='password')
        data = {
            "title": "The Hobbit (Updated)",
            "publication_year": 1937,
            "author": self.author.id
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "The Hobbit (Updated)")

    def test_update_book_unauthenticated(self):
        data = {
            "title": "The Hobbit (Hacked)",
            "publication_year": 1937,
            "author": self.author.id
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='password')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_book_unauthenticated(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class BookFilterTests(APITestCase):
    def setUp(self):
        # Create Authors
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        # Create Books
        self.book1 = Book.objects.create(
            title="First Book",
            publication_year=2020,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Second Book",
            publication_year=2021,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title="Third Book",
            publication_year=2020,
            author=self.author1
        )
        
        self.list_url = reverse('book-list')

    def test_filter_by_publication_year(self):
        response = self.client.get(self.list_url, {'publication_year': 2020})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expecting 2 books published in 2020
        self.assertEqual(len(response.data), 2)
        titles = [book['title'] for book in response.data]
        self.assertIn("First Book", titles)
        self.assertIn("Third Book", titles)

    def test_filter_by_title(self):
        response = self.client.get(self.list_url, {'title': 'First Book'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "First Book")

    def test_filter_by_author(self):
        # Filter by author ID
        response = self.client.get(self.list_url, {'author': self.author1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expecting 2 books by Author One
        self.assertEqual(len(response.data), 2)
        for book in response.data:
            self.assertEqual(book['author'], self.author1.id)

    def test_search_by_title(self):
        response = self.client.get(self.list_url, {'search': 'Second'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Second Book")

    def test_search_by_author_name(self):
        # Searching "Author Two" should return "Second Book"
        response = self.client.get(self.list_url, {'search': 'Author Two'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Second Book")

    def test_ordering_by_publication_year(self):
        response = self.client.get(self.list_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 2020 comes before 2021. Since 2 books have 2020, order between them is not guaranteed unless secondary sort exists.
        # But both should be before 2021.
        self.assertEqual(response.data[0]['publication_year'], 2020)
        self.assertEqual(response.data[1]['publication_year'], 2020)
        self.assertEqual(response.data[2]['publication_year'], 2021)

    def test_ordering_by_title_descending(self):
        response = self.client.get(self.list_url, {'ordering': '-title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # T (Third) > S (Second) > F (First)
        self.assertEqual(response.data[0]['title'], "Third Book")
        self.assertEqual(response.data[1]['title'], "Second Book")
        self.assertEqual(response.data[2]['title'], "First Book")
