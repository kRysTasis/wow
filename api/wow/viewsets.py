from rest_framework import (
    generics,
    permissions,
    authentication,
    status,
    viewsets,
    filters
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .serializers import (
    UserSerializer,
    WowSerializer,
)
from .models import (
    mUser,
    FollowRelationShip,
    FollowRequest,
    LikedRelationShip,
    Category,
    HashTag,
    WordOfWistom,
)

import logging
logger = logging.getLogger(__name__)


class BaseModelViewSet(viewsets.ModelViewSet):

    pass


class UserViewSet(BaseModelViewSet):

    permission_classes = (permissions.AllowAny,)
    queryset = mUser.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
