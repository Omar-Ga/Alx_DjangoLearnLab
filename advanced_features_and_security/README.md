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
    - `SECURE_SSL_REDIRECT = True`: Redirects all non-HTTPS traffic to HTTPS.
    - `SECURE_HSTS_SECONDS = 31536000`: Enforces HTTP Strict Transport Security (HSTS) for 1 year.
    - `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`: Includes subdomains in HSTS policy.
    - `SECURE_HSTS_PRELOAD = True`: Allows preloading of the site into browser HSTS lists.

2.  **CSRF Protection**:
    - All forms in templates use the `{% csrf_token %}` tag.

3.  **Secure Data Access**:
    - Views use Django Forms (`ExampleForm`) to validate and sanitize user input.
    - Django's ORM is used to prevent SQL injection.

4.  **Content Security Policy (CSP)**:
    - A custom middleware `LibraryProject.middleware.CSPMiddleware` sets the `Content-Security-Policy` header to strict defaults (`default-src 'self'; script-src 'self'; style-src 'self';`).

## Deployment Configuration (HTTPS)
To deploy this application securely with HTTPS, you typically use a web server like Nginx or Apache as a reverse proxy.

### Nginx Configuration Example
```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name example.com www.example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
*Note: Obtain SSL certificates using a tool like Certbot (Let's Encrypt).*

## Security Review
The implemented security measures significantly reduce the risk of common web attacks:
- **XSS**: Mitigated by `SECURE_BROWSER_XSS_FILTER` and `CSP`.
- **CSRF**: Mitigated by Django's CSRF protection and `CSRF_COOKIE_SECURE`.
- **Clickjacking**: Prevented by `X_FRAME_OPTIONS = 'DENY'`.
- **Man-in-the-Middle (MITM)**: Prevented by enforcing HTTPS via `SECURE_SSL_REDIRECT` and HSTS settings.
- **Data Integrity**: `SECURE_CONTENT_TYPE_NOSNIFF` ensures browsers interpret files correctly.

Future improvements could include:
- Implementing more granular CSP rules (e.g., specific image sources).
- Regular dependency auditing.
- Implementing rate limiting.
