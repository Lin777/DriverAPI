# file backend/server/apps/endpoints/urls.py

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apps.endpoints.views import PredictView
from . import views

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r"^api/v1/", include(router.urls)),
    # add predict url
    url(r"^api/v1/(?P<endpoint_name>.+)/predict$", PredictView.as_view(), name="predict"),
    url(r"^monitoring/", views.index, name='index'),
]