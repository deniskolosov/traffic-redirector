import string
import random
from .models import LinksLandingPages
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .models import Profile, Link, LandingPage


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


class HomeView(LoginRequiredMixin, TemplateView):
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


class LinkDetailView(LoginRequiredMixin, DetailView):
    slug_field = 'short_url_path__iexact'
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
        context.update(
            {
                'stats': self.object.get_link_stats(),
                'username': self.object.user.user.username
             }
        )
        return context


class LinkCreateView(LoginRequiredMixin, CreateView):
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


class LandingPageCreateView(LoginRequiredMixin, CreateView):
    model = LandingPage
    template_name = 'url_manager/landing-page-create.html'
    fields = ['weight', 'allowed_countries', 'url', 'name']
    success_url = reverse_lazy('home')


class LinksLandingPagesForm(forms.ModelForm):
    class Meta:
        model = LinksLandingPages
        fields = ['link', 'landing_page']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(LinksLandingPagesForm, self).__init__(*args, **kwargs)
        self.fields['link'].queryset = Link.objects.filter(user=user.profile)
        self.fields['landing_page'].queryset = LandingPage.objects.all()


class LinksLandingPagesCreateView(LoginRequiredMixin, CreateView):
    model = LinksLandingPages
    template_name = 'url_manager/link-landing-page-create.html'
    form_class = LinksLandingPagesForm

    def get_form_kwargs(self):
        kwargs = super(LinksLandingPagesCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class LandingPageUpdateView(LoginRequiredMixin, UpdateView):
    model = LandingPage
    fields = ['weight', 'allowed_countries']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('home')


class LandingPageListView(ListView):
    model = LandingPage
    template_name = 'url_manager/landing-pages-list.html'
    context_object_name = 'landing_pages'

