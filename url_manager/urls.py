from django.urls import re_path, path

from . import views

urlpatterns = [
    re_path('^landing-pages/update/(?P<pk>\d+)/$', views.LandingPageUpdateView.as_view(),
            name='landing-page-update'),
    path('list/', views.LandingPageListView.as_view(), name='landing-pages-list'),
]
