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
Example:
```python
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    ...
```
