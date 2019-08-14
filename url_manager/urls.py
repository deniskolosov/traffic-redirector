from django.urls import re_path

from . import views

urlpatterns = [
    re_path('^landing-pages/update/(?P<pk>\d+)/$', views.LandingPageUpdateView.as_view(),
            name='landing-page-update'),
]
