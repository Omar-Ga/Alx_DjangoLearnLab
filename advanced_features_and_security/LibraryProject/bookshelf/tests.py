from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Book, CustomUser

@override_settings(SECURE_SSL_REDIRECT=False)
class PermissionTests(TestCase):
    def setUp(self):
        # Create groups and permissions (similar to setup script)
        self.editors_group = Group.objects.create(name='Editors')
        self.viewers_group = Group.objects.create(name='Viewers')
        self.admins_group = Group.objects.create(name='Admins')

        content_type = ContentType.objects.get_for_model(Book)
        self.can_view = Permission.objects.get(codename='can_view', content_type=content_type)
        self.can_create = Permission.objects.get(codename='can_create', content_type=content_type)
        self.can_edit = Permission.objects.get(codename='can_edit', content_type=content_type)
        self.can_delete = Permission.objects.get(codename='can_delete', content_type=content_type)

        self.editors_group.permissions.add(self.can_create, self.can_edit)
        self.viewers_group.permissions.add(self.can_view)
        self.admins_group.permissions.add(self.can_create, self.can_edit, self.can_delete, self.can_view)

        # Create users
        self.viewer_user = CustomUser.objects.create_user(username='viewer', email='viewer@example.com', password='password')
        self.viewer_user.groups.add(self.viewers_group)

        self.editor_user = CustomUser.objects.create_user(username='editor', email='editor@example.com', password='password')
        self.editor_user.groups.add(self.editors_group)

        self.admin_user = CustomUser.objects.create_user(username='admin_user', email='admin@example.com', password='password')
        self.admin_user.groups.add(self.admins_group)
        
        self.book = Book.objects.create(title='Test Book', author='Test Author', publication_year=2023)

    def test_viewer_permissions(self):
        self.client.login(username='viewer', password='password')
        
        # Should be able to view
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)

        # Should NOT be able to create
        response = self.client.get('/books/create/')
        self.assertEqual(response.status_code, 403)

    def test_editor_permissions(self):
        self.client.login(username='editor', password='password')
        
        # Should be able to create
        response = self.client.get('/books/create/')
        self.assertEqual(response.status_code, 200)
        
        # Should be able to edit
        response = self.client.get(f'/books/{self.book.pk}/edit/')
        self.assertEqual(response.status_code, 200)

        # Should NOT be able to delete
        response = self.client.get(f'/books/{self.book.pk}/delete/')
        self.assertEqual(response.status_code, 403)
