"""tds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from url_manager.views import signup, LinkCreateView, LinkDetailView, HomeView, TemplateView,\
    LandingPageCreateView, LinksLandingPagesCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^signup/$', signup, name='signup'),
    path('', HomeView.as_view(template_name='home.html'), name='home'),
    path('landing1/', TemplateView.as_view(template_name='landing1.html'), name='landing_1'),
    path('landing2/', TemplateView.as_view(template_name='landing2.html'), name='landing_2'),
    path('landing3/', TemplateView.as_view(template_name='landing3.html'), name='landing_3'),
    path('create-link/', LinkCreateView.as_view(), name='create-link'),
    path('create-links-landing-pages/', LinksLandingPagesCreateView.as_view(), name='create-links-landing-pages'),
    path('create-landing-page/', LandingPageCreateView.as_view(), name='create-landing-page'),
    path('links/<slug:short_url_path>/', LinkDetailView.as_view(), name='link-detail'),
    path('landing-pages/', include('url_manager.urls')),

]
