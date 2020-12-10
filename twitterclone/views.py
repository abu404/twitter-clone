from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, CreateAPIView, ListAPIView
from rest_framework import exceptions, permissions
from rest_framework.viewsets import ModelViewSet
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


class TweetLikeView(ModelViewSet):
    serializer_class = TweetLikeSerializer
    queryset = Tweet.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        user_pk = self.request.data['user_id']
        u = User.objects.get(pk=user_pk)
        tweet = self.get_object()
        tweet.likes.add(u)
        tweet.save()
        return Response(data=[dict(id=i.id, name=i.username) for i in tweet.likes.all()])


class TweetUnlikeView(UpdateAPIView):
    serializer_class = TweetLikeSerializer
    queryset = Tweet.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        user_pk = self.request.data['user_id']
        u = User.objects.get(pk=user_pk)
        tweet = self.get_object()
        tweet.likes.remove(u)
        tweet.save()
        return Response(data=[dict(id=i.id, name=i.username) for i in tweet.likes.all()])


class UserFollowView(ModelViewSet):
    serializer_class = FollowingSerializer
    queryset = UserRelationship.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user_relationship = self.get_queryset().first()
        if not user_relationship:
            user_relationship = UserRelationship(user=self.request.user)
            user_relationship.save()

        follow_user = User.objects.get(pk=self.request.data['user_id'])
        user_relationship.following.add(follow_user)
        user_relationship.save()
        users = [i.id for i in user_relationship.following.all()]
        return Response({'following_users': users})


class UserUnfollowView(ModelViewSet):
    serializer_class = FollowingSerializer
    queryset = UserRelationship.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user_relationship = self.get_queryset().first()
        if not user_relationship:
            user_relationship = UserRelationship(user=self.request.user)
            user_relationship.save()

        follow_user = User.objects.get(pk=self.request.data['user_id'])
        user_relationship.following.remove(follow_user)
        user_relationship.save()
        return Response({'current_following': [dict(id=i.id, name=i.username)
                                               for i in user_relationship.following.all()]})


class UserFollowersView(ListAPIView):
    serializer_class = UserFollowersSerializer
    queryset = UserRelationship.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class TweetLikesView(ModelViewSet):
    serializer_class = TweetLikesSerializer
    queryset = Tweet.objects.prefetch_related('likes').all()
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response({'liked_users': [dict(id=i.id, name=i.username) for i in instance.likes.all()]})


