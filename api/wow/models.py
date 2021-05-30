from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.db.models import F
from .core.models import (
    TimeStampModel
)
import os, uuid, logging

logger = logging.getLogger(__name__)


def profile_file_name(instance, filename):
    return 'upload/{0}/{1}/'.format(instance.username, filename)



class BaseModel(TimeStampModel):
    """
    基本モデルのベース
    """
    pass


class UserManager(BaseUserManager):
    """
    カスタマイズユーザーマネージャー
        emailも持たせる
    """

    use_in_migrations = True


    def _create_user(self, username, email, password, **extra_fields):

        if not username:
            raise ValueError('ユーザーネームは必須項目です。')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, email=None, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)



class mUser(AbstractBaseUser,
            PermissionsMixin,
            BaseModel):
    """
    ユーザーモデル
    """

    username = models.CharField(_('Username'), max_length=70, unique=True, blank=True, null=True)
    email = models.EmailField(_('Email'), max_length=70, unique=True)
    icon = models.ImageField(_('Icon'), upload_to=profile_file_name, blank=True, null=True)



    mywow = models.ForeignKey(
        'wow.WordOfWistom',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    followees = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        through='FollowRelationShip',
        through_fields=('followee', 'follower'),
    )

    follow_requests = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        through='FollowRequest',
        through_fields=('follow_request_user', 'follow_response_user'),
        related_name='follow_request_users',
    )

    is_staff = models.BooleanField(
        _('Staff Status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )

    is_active = models.BooleanField(
        _('Active Flag'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def get_username(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class FollowRelationShip(BaseModel):
    """
    フォロー関係の中間テーブル
    """

    followee = models.ForeignKey(
        'wow.mUser',
        on_delete=models.CASCADE,
        related_name='followee'
    )
    follower = models.ForeignKey(
        'wow.mUser',
        on_delete=models.CASCADE,
        related_name='follower'
    )


class FollowRequest(BaseModel):
    """
    フォローリクエストの中間テーブル
    """

    follow_request_user = models.ForeignKey(
        'wow.mUser',
        on_delete=models.CASCADE,
        related_name='follow_request_user'
    )
    follow_response_user = models.ForeignKey(
        'wow.mUser',
        on_delete=models.CASCADE,
        related_name='follow_response_user'
    )
    isAccepted = models.BooleanField(default=False)


class LikedRelationShip(BaseModel):
    """
    いいねの中間テーブル
    """

    liked_wow = models.ForeignKey(
        'wow.WordOfWistom',
        on_delete=models.CASCADE,
        related_name='liked_wow'
    )
    liked_user = models.ForeignKey(
        'wow.mUser',
        on_delete=models.CASCADE,
        related_name='liked_user'
    )


class Category(models.Model):

    name = models.CharField(_('Category'), max_length=50)
    slug = models.SlugField(default=name)

    def __str__(self):
        return self.name


class HashTag(BaseModel):

    title = models.CharField(_('Title'), max_length=30)
    slug = models.SlugField(_('Slug'), blank=True, null=True)

    def __str__(self):
        return self.title


class WordOfWistom(BaseModel):
    """
    名言
    """

    content = models.TextField()
    author = models.ForeignKey(
        'wow.mUser',
        on_delete=models.CASCADE,
    )
    liked = models.ManyToManyField(
        mUser,
        blank=True,
        through='LikedRelationShip',
        related_name='liked'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    hashTag = models.ManyToManyField(
        HashTag,
        blank=True,
    )

    def __str__(self):
        return self.content

    class Meta:
        indexes = [
            models.Index(fields=['category', 'content']),
            models.Index(fields=['author', 'content'])
        ]
