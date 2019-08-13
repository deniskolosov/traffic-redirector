# books/urls.py
from django.urls import path, re_path, include

from . import views

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('<slug:short_url_path>/', views.LinkDetailView.as_view(), name='link-detail'),
    re_path('^landing-pages/update/(?P<pk>\d+)/$', views.LandingPageUpdateView.as_view(),
            name='landing-page-update'),
]
