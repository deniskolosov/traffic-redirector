from django.contrib import admin
from .models import LandingPage, Link, Visit, LinksLandingPages, Profile

# Register your models here.
admin.site.register(LandingPage)
admin.site.register(Link)
admin.site.register(Visit)
admin.site.register(LinksLandingPages)
admin.site.register(Profile)
