from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class PostTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.post_data = {'title': 'Test Post', 'content': 'Test Content'}

    def test_create_post(self):
        url = reverse('post-list')
        response = self.client.post(url, self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().author, self.user)

    def test_get_posts(self):
        Post.objects.create(author=self.user, title='Post 1', content='Content 1')
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check for results key because of pagination
        self.assertIn('results', response.data)

    def test_update_post_author(self):
        post = Post.objects.create(author=self.user, title='Old Title', content='Old Content')
        url = reverse('post-detail', kwargs={'pk': post.pk})
        response = self.client.patch(url, {'title': 'New Title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, 'New Title')

    def test_update_post_not_author(self):
        post = Post.objects.create(author=self.other_user, title='Other Title', content='Other Content')
        url = reverse('post-detail', kwargs={'pk': post.pk})
        response = self.client.patch(url, {'title': 'New Title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_author(self):
        post = Post.objects.create(author=self.user, title='To Delete', content='Content')
        url = reverse('post-detail', kwargs={'pk': post.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_create_comment(self):
        post = Post.objects.create(author=self.user, title='Post', content='Content')
        url = reverse('comment-list')
        response = self.client.post(url, {'post': post.pk, 'content': 'Test Comment'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().author, self.user)
