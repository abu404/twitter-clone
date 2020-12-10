from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
import jwt
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from twitterclone.models import UserRelationship, Tweet
# Create your tests here.


class TestViews(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.auth_user = User.objects.create_user("unittestuser", email="test@unittestuser.com")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_token()}")
        self.tweet_id = self.tweet_create()
        self.newuser = User.objects.create_user(username='tweetliker', email="tweetliker@tweetliker.com")
        self.user_relationship = UserRelationship.objects.create(user=self.auth_user)
        self.user_relationship.save()
        self.user_relationship.following.add(self.newuser)
        self.user_relationship.save()
        # self.tweet = Tweet.objects.get(pk=self.tweet_id)

    def get_token(self):
        tok = jwt.encode(dict(username="unittestuser"), settings.JWT_SECRET)
        return tok.decode('utf-8')

    def tweet_create(self):
        data = {
            "content": "unit test",
            "is_retweet": False
        }
        url = reverse('tweet-list-create')
        response = self.client.post(url, data=data)
        # print("response", response.json())
        response_data = response.json()
        return response_data['id']

    def test_list_tweet(self):
        print("[*] Testing tweet list")
        url = reverse('tweet-list-create')
        response = self.client.get(url)
        # print("resp", response.json())
        self.assertEqual(len(response.json()), 1)

    def test_tweet_like(self):
        print("[*] Testing like a tweet ")

        data = {
            'user_id': self.newuser.id
        }
        response = self.client.put(reverse('tweet-like', kwargs={'id': self.tweet_id}), data=data)
        self.assertEqual(response.status_code, 200)

    def test_get_tweet_likers(self):
        data = {
            'user_id': self.newuser.id
        }
        self.client.put(reverse('tweet-like', kwargs={'id': self.tweet_id}), data=data)
        url = reverse('get_tweet_likes', kwargs={'id': self.tweet_id})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(len(data['liked_users']), 1)

    def test_tweet_unlike(self):
        print("[*] Testing unliking a tweet")
        data = {
            'user_id': self.newuser.id
        }
        response = self.client.put(reverse('tweet-unlike', kwargs={'id': self.tweet_id}), data=data)
        self.assertEqual(response.status_code, 200)

    def test_user_follow(self):
        print("[*] Testing user follow")
        data = {
            'user_id': self.newuser.id
        }
        response = self.client.post(reverse('follow'), data=data)
        self.assertEqual(response.status_code, 200)

    def test_following_for_user(self):
        print("[*] Testing get user followers")
        data = {
            'user_id': self.newuser.id
        }
        self.client.post(reverse('follow'), data=data)
        response = self.client.get(reverse('user-following'))
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(len(data[0]['following']), 1)

    def test_user_unfollow(self):
        print("[*] Testing user unfollow")
        data = {
            'user_id': self.newuser.id
        }
        response = self.client.post(reverse('unfollow'), data=data)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('user-following'))
        data = response.json()
        self.assertEqual(len(data[0]['following']), 0)
