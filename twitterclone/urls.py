from django.urls import path, include

from .views import TweetListView, TweetLikeView, TweetUnlikeView, UserFollowView, UserUnfollowView, UserFollowersView, TweetLikesView
put_mapping = dict(put='update')
get_mapping = dict(get='retrieve')
post_mapping = dict(post='create')
urlpatterns = [
    path('tweet', TweetListView.as_view(), name='tweet-list-create'),
    path('tweet/like/<int:id>', TweetLikeView.as_view(put_mapping), name='tweet-like'),
    path('tweet/unlike/<int:id>', TweetUnlikeView.as_view(), name='tweet-unlike'),
    path('tweet/likes/<int:id>', TweetLikesView.as_view(get_mapping), name='get_tweet_likes'),
    path('user/follow', UserFollowView.as_view(post_mapping), name='follow'),
    path('user/unfollow', UserUnfollowView.as_view(post_mapping), name='unfollow'),
    path('user/following', UserFollowersView.as_view(), name='user-following'),
]
