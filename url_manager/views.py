import string
import random
from .models import LandingPage, LinksLandingPages, Link, Visit
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView
from django.urls import reverse_lazy
from django import forms
from django.shortcuts import render
from .models import Profile, Link, LandingPage


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        links = Profile.objects.get(user__id=user.id).links.prefetch_related('links_landing_pages')
        links_landing_pages = {l: [obj.landing_page for obj in l.links_landing_pages.all()] for l in links}
        links_visits = {link: link.visits.all() for link in links}
        context.update(
            {'links_landing_pages': links_landing_pages,
             'links_visits': links_visits}
        )

        return context


class LinkDetailView(DetailView):
    slug_field = 'short_url_path'
    slug_url_kwarg = 'short_url_path'
    template_name = 'link.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Link.objects.filter(user=self.request.user.profile)
        else:
            return Link.objects.none()

    def get_context_data(self, **kwargs):
        context = super(LinkDetailView, self).get_context_data(**kwargs)
        context['stats'] = self.object.get_link_stats()
        return context


class LinkCreateView(CreateView):
    model = Link
    template_name = 'url_manager/link-create.html'
    fields = ['short_url_path']
    success_url = reverse_lazy('create-links-landing-pages')

    def get_initial(self, *args, **kwargs):
        initial = super(LinkCreateView, self).get_initial(**kwargs)
        initial['short_url_path'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return initial

    def form_valid(self, form):
        short_url_path = form.cleaned_data['short_url_path']
        if Link.objects.filter(short_url_path=short_url_path).exists():
            form.add_error('short_url_path',
                           'This sequence exists already, please save the form again with new sequence')
            return self.form_invalid(form)
        obj = form.save(commit=False)
        obj.user = self.request.user.profile
        obj.save()
        return super(LinkCreateView, self).form_valid(form)


class LinksLandingPagesCreateView(CreateView):
    model = LinksLandingPages
    template_name = 'url_manager/link-landing-page-create.html'
    fields = ['link', 'landing_page']


class LandingPageUpdateView(UpdateView):
    model = LandingPage
    fields = ['weight', 'allowed_countries']
    template_name_suffix = '_update_form'
