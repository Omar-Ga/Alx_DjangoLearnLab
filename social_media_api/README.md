# Social Media API

This project is a Django-based Social Media API using Django REST Framework.

## Setup

1.  Clone the repository.
2.  Navigate to `social_media_api`.
3.  Install dependencies:
    ```bash
    pip install django djangorestframework Pillow
    ```
4.  Run migrations:
    ```bash
    python manage.py migrate
    ```
5.  Run the server:
    ```bash
    python manage.py runserver
    ```

## User Model

The project uses a custom user model `accounts.CustomUser` extending `AbstractUser`.
It includes additional fields:
-   `bio`: TextField
-   `profile_picture`: ImageField
-   `followers`: ManyToManyField to 'self' (symmetrical=False)

## Authentication

The API uses Token Authentication.

### Register
**Endpoint:** `POST /api/register/`
**Body:**
```json
{
    "username": "yourusername",
    "password": "yourpassword",
    "email": "email@example.com",
    "bio": "Optional bio",
    "profile_picture": (optional file)
}
```
**Response:**
Returns the created user data and an authentication token.

### Login
**Endpoint:** `POST /api/login/`
**Body:**
```json
{
    "username": "yourusername",
    "password": "yourpassword"
}
```
**Response:**
Returns the authentication token.

### Profile
**Endpoint:** `GET /api/profile/`
**Headers:**
`Authorization: Token <your_token>`
**Response:**
Returns the authenticated user's profile data.
