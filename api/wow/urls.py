from django.urls import path, include
from . import views, viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', viewsets.UserViewSet)


app_name = 'wow'
urlpatterns = [
    path('', include(router.urls)),
]
