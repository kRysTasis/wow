from rest_framework import serializers
from .models import (
    mUser,
    WordOfWistom,
)
import logging


logging.basicConfig(
    level = logging.DEBUG,
    format = '''%(levelname)s %(asctime)s %(pathname)s:%(funcName)s:%(lineno)s
    %(message)s''')

logger = logging.getLogger(__name__)



class SubUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = mUser
        fields = [
            'pk',
            'username',
            'email',
            'created_at',
            'icon',
        ]


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=False)
    followees = SubUserSerializer(many=True)
    followers = serializers.SerializerMethodField()
    followees_count = serializers.IntegerField(source='followees.count')
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = mUser
        fields = [
            'pk',
            'username',
            'email',
            'password',
            'followees',
            'followers',
            'followees_count',
            'followers_count',
        ]

    def get_followers(self, obj):
        return SubUserSerializer(mUser.objects.filter(followees=obj), many=True).data

    def get_followers_count(self, obj):
        return len(self.get_followers(obj)) if self.get_followers(obj) != None else 0


class WowSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')
    author_pk = serializers.CharField(required=False)

    class Meta:
        model = WordOfWistom
        fields = [
            'pk',
            'author',
            'author_pk',
            'content',
        ]
