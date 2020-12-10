from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Tweet(models.Model):
    content = models.CharField(max_length=280)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    is_retweet = models.BooleanField(default=False)
    likes = models.ManyToManyField(to=User, related_name="tweet_likes")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class UserRelationship(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    followers = models.ManyToManyField(to=User, related_name="user_followers")
    following = models.ManyToManyField(to=User, related_name="user_following")

    def __str__(self):
        return self.user.first_name


class TweetLike(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    tweet = models.ForeignKey(Tweet, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now=True)
    # objects = TweetLikeManager()

    def __str__(self):
        return f"TweetLike {self.user.pk} - {self.tweet.pk}"
