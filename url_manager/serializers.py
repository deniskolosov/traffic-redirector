from .models import LandingPage, LinksLandingPages, Link, Visit
from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin


class LandingPageSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = LandingPage
        fields = ['url', 'name', 'weight', 'allowed_countries']


class LinksLandingPagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinksLandingPages
        fields = ['link', 'landing_page']


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['short_url_path']


class VisitSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ['ip_address', 'link', 'country', 'created_at']
