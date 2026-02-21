from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like
from notifications.models import Notification

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

    def test_like_post(self):
        post = Post.objects.create(author=self.other_user, title='Title', content='Content')
        url = reverse('like_post', kwargs={'pk': post.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
        # Check notification
        notification = Notification.objects.filter(recipient=self.other_user, actor=self.user, verb='liked your post').first()
        self.assertIsNotNone(notification)

    def test_unlike_post(self):
        post = Post.objects.create(author=self.other_user, title='Title', content='Content')
        Like.objects.create(user=self.user, post=post)
        url = reverse('unlike_post', kwargs={'pk': post.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 0)

    def test_comment_notification(self):
        post = Post.objects.create(author=self.other_user, title='Title', content='Content')
        url = reverse('comment-list')
        self.client.post(url, {'post': post.pk, 'content': 'Nice post!'})
        notification = Notification.objects.filter(recipient=self.other_user, actor=self.user, verb='commented on your post').first()
        self.assertIsNotNone(notification)

    def test_follow_notification(self):
        url = reverse('follow_user', kwargs={'user_id': self.other_user.pk})
        self.client.post(url)
        notification = Notification.objects.filter(recipient=self.other_user, actor=self.user, verb='started following you').first()
        self.assertIsNotNone(notification)

    def test_get_notifications(self):
        Notification.objects.create(recipient=self.user, actor=self.other_user, verb='liked your post')
        url = reverse('notifications')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
