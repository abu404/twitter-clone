from rest_framework import serializers
from .models import *


# class TweetLikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = '__all__'
#         model = TweetLike
#

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'content']
        model = Tweet


class TweetLikeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        fields = ['user_id']
        model = Tweet


class TweetLikeResponseSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        fields = ['user_id']
        model = Tweet


class FollowingSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        fields = ['user_id']
        model = UserRelationship


class UserFollowersSerializer(serializers.ModelSerializer):
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        fields = ['following']
        model = User


class TweetLikesSerializer(serializers.ModelSerializer):
    likes = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        fields = ['likes']
        model = User


