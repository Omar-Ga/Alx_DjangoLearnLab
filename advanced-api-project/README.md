# Advanced API Project

This project implements a book API using Django and Django REST Framework.

## Models
- **Author**: Represents a book author.
- **Book**: Represents a book, linked to an Author.

## API Endpoints

The API provides the following endpoints for managing books:

- **List Books**: `GET /api/books/`
  - Retrieves a list of all books.
  - Access: Public (Read-only)

- **Book Detail**: `GET /api/books/<int:pk>/`
  - Retrieves details of a specific book by ID.
  - Access: Public (Read-only)

- **Create Book**: `POST /api/books/create/`
  - Creates a new book.
  - Access: Authenticated users only.

- **Update Book**: `PUT/PATCH /api/books/update/<int:pk>/`
  - Updates an existing book.
  - Access: Authenticated users only.

- **Delete Book**: `DELETE /api/books/delete/<int:pk>/`
  - Deletes a book.
  - Access: Authenticated users only.

## Permissions

- **Unauthenticated users** can view the list of books and book details.
- **Authenticated users** can create, update, and delete books.

## Setup
1. Clone the repository.
2. Install dependencies: `pip install django djangorestframework`.
3. Run migrations: `python manage.py migrate`.
4. Start the server: `python manage.py runserver`.
