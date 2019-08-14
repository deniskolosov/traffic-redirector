import datetime
from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.urls import reverse

# TODO: select hostname from settings
HOSTNAME = settings.TDS_HOSTNAME
URL_CHOICES = [
    (HOSTNAME + 'landing1/', HOSTNAME + 'landing1/'),
    (HOSTNAME + 'landing2/', HOSTNAME + 'landing2/'),
    (HOSTNAME + 'landing3/', HOSTNAME + 'landing3/'),
]


class LandingPage(models.Model):
    url = models.URLField(choices=URL_CHOICES)
    name = models.CharField(max_length=256)
    weight = models.IntegerField()
    allowed_countries = CountryField(multiple=True, blank_label='(select country)')

    def get_absolute_url(self):
        return reverse('landing-page-update', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Link(models.Model):
    short_url_path = models.CharField(max_length=256, primary_key=True)
    user = models.ForeignKey(Profile, related_name='links', on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.short_url_path

    def get_absolute_url(self):
        return reverse('link-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.short_url_path)
        super().save(*args, **kwargs)

    def get_link_stats(self):
        visits_qs = self.visits.all()
        # total amt of clicks, unique clicks,
        # distribution over time (hourly data for past 24h)
        chart_data = []
        total_clicks = visits_qs.count()
        unique_clicks = len(visits_qs.values('ip_address').distinct())

        date_from = datetime.datetime.now() - datetime.timedelta(hours=24)
        for i in range(24):
            current_date_from = date_from + datetime.timedelta(hours=i)
            chart_data.append(visits_qs.filter(
                created_at__gte=current_date_from,
                created_at__lt=current_date_from+datetime.timedelta(hours=1)).count()
            )

        stats = {
            "total_clicks": total_clicks,
            "unique_clicks": unique_clicks,
            "chart_data": chart_data
        }

        return stats


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class LinksLandingPages(models.Model):
    link = models.ForeignKey(Link, related_name='links_landing_pages', on_delete=models.CASCADE)
    landing_page = models.ForeignKey(LandingPage, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('home')


class Visit(models.Model):
    ip_address = models.GenericIPAddressField()
    link = models.ForeignKey(Link, related_name='visits', on_delete=models.CASCADE)
    country = CountryField(blank_label='(select country)')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Visit from {} to {} at {}".format(self.ip_address, self.link, self.created_at)

