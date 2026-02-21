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

## Posts and Comments

All endpoints are at `/api/posts/` and `/api/comments/`.

### Posts

-   `GET /api/posts/`: List posts (paginated, searchable by `title` and `content`).
-   `POST /api/posts/`: Create a post.
-   `GET /api/posts/{id}/`: Retrieve a post.
-   `PUT /api/posts/{id}/`: Update a post (author only).
-   `PATCH /api/posts/{id}/`: Partially update a post (author only).
-   `DELETE /api/posts/{id}/`: Delete a post (author only).

### Comments

-   `GET /api/comments/`: List comments.
-   `POST /api/comments/`: Create a comment.
-   `GET /api/comments/{id}/`: Retrieve a comment.
-   `PUT /api/comments/{id}/`: Update a comment (author only).
-   `PATCH /api/comments/{id}/`: Partially update a comment (author only).
-   `DELETE /api/comments/{id}/`: Delete a comment (author only).

## Filtering

Posts can be searched using the `search` query parameter:
-   `GET /api/posts/?search=keyword`

## Follows and Feed

### Follow/Unfollow

-   `POST /api/follow/{user_id}/`: Follow a user.
-   `POST /api/unfollow/{user_id}/`: Unfollow a user.

### Feed

-   `GET /api/feed/`: Retrieve a feed of posts from followed users (paginated).

## Likes and Notifications

### Likes

-   `POST /api/posts/{id}/like/`: Like a post.
-   `POST /api/posts/{id}/unlike/`: Unlike a post.

### Notifications

-   `GET /api/notifications/`: Fetch your notifications (paginated).

## Deployment

This project is configured for deployment to platforms like Heroku, Render, or any VPS with Gunicorn.

### Steps to Deploy

1.  **Set Environment Variables:**
    -   `SECRET_KEY`: A strong unique key.
    -   `DEBUG`: `False` for production.
    -   `ALLOWED_HOSTS`: List of domains.
    -   `DATABASE_URL`: Connection string for your production database.
    -   `SECURE_SSL_REDIRECT`: `True` to force HTTPS.

2.  **Static Files:**
    The project uses `WhiteNoise` to serve static files. Run `python manage.py collectstatic` during deployment.

3.  **Database:**
    Run migrations on the production server:
    ```bash
    python manage.py migrate
    ```

4.  **Web Server:**
    The project uses `Gunicorn`. The `Procfile` is included for process management.

### Live URL
(Example: https://social-media-api-django.herokuapp.com/)
