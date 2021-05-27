from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from rest_framework_jwt.views import obtain_jwt_token

from . import settings

urlpatterns = [
    path('wow/', include('wow.urls')),
    path('admin/', admin.site.urls),
    path('auth/', obtain_jwt_token),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
