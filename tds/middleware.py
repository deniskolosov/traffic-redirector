import geoip2.database
from collections import defaultdict
from geoip2.errors import AddressNotFoundError
from django.http import HttpResponseRedirect
from url_manager.models import Link, Visit, LandingPage, LinksLandingPages
import random
from django.core.exceptions import ObjectDoesNotExist


def get_country_from_ip(ip_address):
    # TODO: move initialisation to where the app starts
    import os
    reader = geoip2.database.Reader('./tds/GeoLite2-Country.mmdb')
    country_name = ''
    try:
        response = reader.country(ip_address)
        country_name = response.country.iso_code
    except AddressNotFoundError:
        # country_name = 'Unknown'
        # TODO: testing
        country_name = 'GB'

    return country_name


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def select_redirect_page(weights_urls):
    """
    Select and return url based on weights.
    :param weights_urls: Dict in format {1: ['https://127.0.0.1']} to choose redirect page
     from depending on weight and country.
    :return:  Url to redirect to.
    """
    weights = weights_urls.keys()
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return random.choice(weights_urls[w])


class LocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        ip_address = get_client_ip(request)
        country_name = get_country_from_ip(ip_address)
        path = request.path.split('/')[1]
        path_link = None
        try:
            path_link = Link.objects.get(short_url_path=path)
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                request.META['REMOTE_ADDR'] = request.META['HTTP_X_FORWARDED_FOR']

            # Search path in db and fetch weights
            path_link = Link.objects.get(short_url_path=path)
            landing_pages = LinksLandingPages.objects.prefetch_related(
                'link', 'landing_page').filter(
                link__short_url_path=path,
                landing_page__allowed_countries__icontains=country_name
            ).values(
                'landing_page__url',
                'landing_page__weight'
            )
            weights_urls = defaultdict(list)
            for page in landing_pages:
                weights_urls[page['landing_page__weight']].append(page['landing_page__url'])

            # Choose where to redirect depending on landing page weight and country.
            redirect_to_url = select_redirect_page(weights_urls)

            # Create a Visit record for current user.
            Visit.objects.create(
                ip_address=ip_address,
                link=path_link,
                country=country_name,
            )

            return HttpResponseRedirect(redirect_to_url)

        except ObjectDoesNotExist:
            # Break the redirect loop.
            response = self.get_response(request)
            return response


