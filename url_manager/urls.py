# books/urls.py
from django.urls import path, re_path, include

from . import views

urlpatterns = [
    re_path('^landing-pages/update/(?P<pk>\d+)/$', views.LandingPageUpdateView.as_view(),
            name='landing-page-update'),
]
