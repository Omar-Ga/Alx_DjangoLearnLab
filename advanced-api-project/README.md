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

## Filtering, Searching, and Ordering

The API supports advanced query capabilities on the Book list endpoint (`/api/books/`).

### Filtering
You can filter books by exact matches on the following fields:
- `title`
- `author`
- `publication_year`

**Example:**
`GET /api/books/?publication_year=2020`

### Searching
You can perform a text search on the following fields:
- `title`
- `author__name`

**Example:**
`GET /api/books/?search=Harry`

### Ordering
You can order the results by the following fields:
- `title`
- `publication_year`

Use a hyphen (`-`) for descending order.

**Example:**
`GET /api/books/?ordering=-publication_year`

## Testing

The project includes a comprehensive suite of unit tests to ensure the API's integrity and correctness.

### Testing Strategy
- **CRUD Operations**: Verified that all endpoints (List, Detail, Create, Update, Delete) perform their intended actions correctly.
- **Permissions**: Confirmed that `IsAuthenticatedOrReadOnly` and `IsAuthenticated` permissions are correctly enforced.
- **Filtering, Searching, and Ordering**: Validated that query parameters for filtering, searching, and ordering produce the expected results.
- **Data Validation**: (Via Serializers) Ensured that invalid data (e.g., future publication years) is rejected.

### Running Tests
To run the tests, execute the following command from the `advanced-api-project` directory:

```bash
python manage.py test api
```

The tests are located in `api/test_views.py`.
