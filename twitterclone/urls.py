from django.urls import path, include

from .views import TweetListView, TweetLikeView, TweetUnlikeView, UserFollowView, UserUnfollowView, UserFollowersView, TweetLikesView
urlpatterns = [
    path('tweet', TweetListView.as_view(), name='tweet-list-create'),
    path('tweet/like/<int:id>', TweetLikeView.as_view(), name='tweet-like'),
    path('tweet/unlike/<int:id>', TweetUnlikeView.as_view(), name='tweet-unlike'),
    path('tweet/likes/<int:id>', TweetLikesView.as_view(), name='get_tweet_likes'),
    path('user/follow', UserFollowView.as_view(), name='follow'),
    path('user/unfollow', UserUnfollowView.as_view(), name='unfollow'),
    path('user/following', UserFollowersView.as_view(), name='user-following'),
]
