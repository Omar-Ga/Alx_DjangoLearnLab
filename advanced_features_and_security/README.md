# Advanced Features and Security

## Custom User Model
This project uses a custom user model `CustomUser` extending `AbstractUser`.
- Fields: `date_of_birth`, `profile_photo`.
- Manager: `CustomUserManager`.

## Permissions and Groups
Custom permissions have been defined for the `Book` model in `bookshelf/models.py`:
- `can_view`: Allows viewing book details.
- `can_create`: Allows creating new books.
- `can_edit`: Allows editing existing books.
- `can_delete`: Allows deleting books.

### Groups
Three groups are configured with specific permissions:
1.  **Viewers**: Can only view books (`can_view`).
2.  **Editors**: Can create and edit books (`can_create`, `can_edit`).
3.  **Admins**: Have full control (`can_view`, `can_create`, `can_edit`, `can_delete`).

### Usage
Permissions are enforced in `bookshelf/views.py` using the `@permission_required` decorator.

## Security Best Practices
Several security measures have been implemented to protect the application:

1.  **Secure Settings**:
    - `DEBUG = False`: Disabled for production safety.
    - `SECURE_BROWSER_XSS_FILTER = True`: Enables the browser's XSS filter.
    - `X_FRAME_OPTIONS = 'DENY'`: Prevents clickjacking by denying framing.
    - `SECURE_CONTENT_TYPE_NOSNIFF = True`: Prevents browser MIME-type sniffing.
    - `CSRF_COOKIE_SECURE = True`: Ensures CSRF cookies are only sent over HTTPS.
    - `SESSION_COOKIE_SECURE = True`: Ensures session cookies are only sent over HTTPS.

2.  **CSRF Protection**:
    - All forms in templates use the `{% csrf_token %}` tag.

3.  **Secure Data Access**:
    - Views use Django Forms (`ExampleForm`) to validate and sanitize user input.
    - Django's ORM is used to prevent SQL injection.

4.  **Content Security Policy (CSP)**:
    - A custom middleware `LibraryProject.middleware.CSPMiddleware` sets the `Content-Security-Policy` header to strict defaults (`default-src 'self'; script-src 'self'; style-src 'self';`).