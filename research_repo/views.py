from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin,PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import Publication, User, AccessGrant
from django.db.models import Q
from .forms import PublicationForm, AuthorshipFormSet, SignUpForm, LoginForm, UploadDocumentForm,AccessGrantForm



class LoginView(LoginView):
    template_name = 'research_repo/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('publication-list')

    def get_queryset(self):
        return Publication.objects.filter(is_public=True)

class LogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('login')

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'research_repo/signup.html'
    success_url = reverse_lazy('login')


class PublicationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Publication
    template_name = 'research_repo/publication_list.html'
    context_object_name = 'publications'

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return Publication.objects.filter(
                Q(is_public=True) |
                Q(grants__viewer=user,
                  grants__access_granted=True,
                  grants__expires_at__gt=timezone.now()) |
                Q(uploader=user) |
                Q(authors__user=user)
            ).distinct()

        return Publication.objects.filter(is_public=True)

    def test_func(self):
        return self.request.user.is_authenticated
    

class PublicationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Publication
    template_name = 'research_repo/publication_detail.html'
    context_object_name = 'publication'

    def test_func(self):
        publication = self.get_object()
        user = self.request.user

        # public publication
        if publication.is_public:
            return True

        # authenticated access rules
        return (
            publication.uploader == user or
            publication.authors.filter(user=user).exists() or
            publication.grants.filter(
                viewer=user,
                access_granted=True,
                expires_at__gt=timezone.now()
            ).exists()
        )
    
class PublicationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Publication
    form_class = PublicationForm
    template_name = 'research_repo/publication_form.html'
    success_url = reverse_lazy('publication_list')

    def test_func(self):
        return self.request.user.can_upload()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data['authorship_formset'] = AuthorshipFormSet(self.request.POST)
        else:
            data['authorship_formset'] = AuthorshipFormSet()

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        authorship_formset = context['authorship_formset']

        if authorship_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.uploader = self.request.user
            self.object.save()

            authorship_formset.instance = self.object
            authorship_formset.save()

            return super().form_valid(form)

        return self.form_invalid(form)
    
class PublicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Publication
    form_class = PublicationForm
    template_name = 'research_repo/publication_form.html'
    success_url = reverse_lazy('publication_list')

    def test_func(self):
        publication = self.get_object()
        return self.request.user == publication.uploader or publication.authors.filter(user=self.request.user).exists()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data['authorship_formset'] = AuthorshipFormSet(self.request.POST, instance=self.object)
        else:
            data['authorship_formset'] = AuthorshipFormSet(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        authorship_formset = context['authorship_formset']

        if authorship_formset.is_valid():
            self.object = form.save()
            authorship_formset.instance = self.object
            authorship_formset.save()

            return super().form_valid(form)

        return self.form_invalid(form)
    
class PublicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Publication
    success_url = reverse_lazy('publication_list')

    def test_func(self):
        publication = self.get_object()
        return self.request.user == publication.uploader or publication.authors.filter(user=self.request.user).exists()
    
class UploadDocumentView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = UploadDocumentForm
    template_name = 'research_repo/upload_document.html'
    success_url = reverse_lazy('publication_list')

    def test_func(self):
        return self.request.user.can_upload()
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.uploader = self.request.user
        self.object.save()
        return super().form_valid(form)

class AccessGrantCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = AccessGrant
    form_class = AccessGrantForm
    template_name = 'research_repo/access_grant_form.html'
    success_url = reverse_lazy('publication_list')

    def get_publication(self):
        if not hasattr(self, "_publication"):
            self._publication = get_object_or_404(
                Publication,
                id=self.kwargs.get('publication_id')
            )
        return self._publication

    def test_func(self):
        publication = self.get_publication()
        user = self.request.user

        return (
            publication.uploader == user or
            publication.authors.filter(user=user).exists()
        )

    def form_valid(self, form):
        form.instance.publication = self.get_publication()
        return super().form_valid(form)