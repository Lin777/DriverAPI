# backend/server/server/urls.py file
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from apps.endpoints.urls import urlpatterns as endpoints_urlpatterns
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.ServerAuth.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += endpoints_urlpatterns