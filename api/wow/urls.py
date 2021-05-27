from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

app_name = 'wow'
urlpatterns = [
    path('', include(router.urls)),
]
