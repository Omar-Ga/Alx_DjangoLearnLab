from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class UserAuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'bio': 'Test bio'
        }
        self.user = User.objects.create_user(username='user1', password='password123')
        self.other_user = User.objects.create_user(username='user2', password='password123')

    def test_register_user(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'new@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_login_user(self):
        response = self.client.post(self.login_url, {
            'username': 'user1',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_follow_unfollow(self):
        self.client.force_authenticate(user=self.user)
        follow_url = reverse('follow_user', kwargs={'user_id': self.other_user.pk})
        unfollow_url = reverse('unfollow_user', kwargs={'user_id': self.other_user.pk})

        # Follow
        response = self.client.post(follow_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.following.filter(pk=self.other_user.pk).exists())

        # Unfollow
        response = self.client.post(unfollow_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user.following.filter(pk=self.other_user.pk).exists())

    def test_feed(self):
        # user1 follows user2
        self.user.following.add(self.other_user)
        # user2 creates a post
        Post.objects.create(author=self.other_user, title='User 2 Post', content='Hello')
        
        self.client.force_authenticate(user=self.user)
        feed_url = reverse('post_feed')
        response = self.client.get(feed_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'User 2 Post')
