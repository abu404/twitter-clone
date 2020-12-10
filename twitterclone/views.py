from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, CreateAPIView, ListAPIView
from rest_framework import exceptions, permissions
from .models import TweetLike, Tweet, UserRelationship, User
from .serializers import *


class TweetListView(ListCreateAPIView):
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response(data=serializer.data)


class TweetLikeView(UpdateAPIView):
    serializer_class = TweetLikeSerializer
    queryset = Tweet.objects.all()
    lookup_field = 'id'

    def perform_update(self, serializer):
        user_pk = serializer.data['user_id']
        u = User.objects.get(pk=user_pk)
        tweet = self.get_object()
        tweet.likes.add(u)
        tweet.save()


class TweetUnlikeView(UpdateAPIView):
    serializer_class = TweetLikeSerializer
    queryset = Tweet.objects.all()
    lookup_field = 'id'

    def perform_update(self, serializer):
        user_pk = serializer.data['user_id']
        u = User.objects.get(pk=user_pk)
        tweet = self.get_object()
        tweet.likes.remove(u)
        tweet.save()


class UserFollowView(CreateAPIView):
    serializer_class = FollowingSerializer
    queryset = UserRelationship.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        user_relationship = self.get_queryset().first()
        if not user_relationship:
            user_relationship = UserRelationship(user=self.request.user)
            user_relationship.save()

        follow_user = User.objects.get(pk=self.request.data['user_id'])
        user_relationship.following.add(follow_user)
        user_relationship.save()
        return Response({'user_id': self.request.data['user_id']})


class UserUnfollowView(CreateAPIView):
    serializer_class = FollowingSerializer
    queryset = UserRelationship.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        user_relationship = self.get_queryset().first()
        if not user_relationship:
            user_relationship = UserRelationship(user=self.request.user)
            user_relationship.save()

        follow_user = User.objects.get(pk=self.request.data['user_id'])
        user_relationship.following.remove(follow_user)
        user_relationship.save()
        return Response({'user_id': self.request.data['user_id']})


class UserFollowersView(ListAPIView):
    serializer_class = UserFollowersSerializer
    queryset = UserRelationship.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class TweetLikesView(ListAPIView):
    serializer_class = TweetLikesSerializer
    queryset = Tweet.objects.prefetch_related('likes').all()
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'

