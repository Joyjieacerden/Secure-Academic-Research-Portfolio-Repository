from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin,PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from honeypot.decorators import check_honeypot
from django_ratelimit.decorators import ratelimit
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from .models import Publication, User, AccessGrant
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
from .forms import PublicationForm, AuthorshipFormSet, SignUpForm, LoginForm, UploadDocumentForm,AccessGrantForm


@method_decorator(check_honeypot, name='dispatch')
@method_decorator(ratelimit(key='ip', rate='10/m', method='POST', block=True), name='dispatch')

class LoginView(LoginView):
    template_name = 'research_repo/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('publication_list')

    def get_queryset(self):
        return Publication.objects.filter(is_public=True)

class LogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('login')
    
    
@method_decorator(check_honeypot, name='dispatch')
@method_decorator(ratelimit(key='ip', rate='5/h', method='POST', block=True), name='dispatch')
class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'research_repo/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # 1. Save the user
        user = form.save(commit=False)
        user.is_active = True  # Allow login immediately for testing
        user.is_email_verified = True  # Mark as verified for testing
        user.save()
        
        # Redirect to login page
        return redirect('login')

class VerifyEmailView(View):
    def get(self, request, token, *args, **kwargs):
        # We use filter() instead of get_object_or_404 to handle errors gracefully
        user = get_object_or_404(User, email_verification_token=token)
        
        user.is_active = True
        user.is_email_verified = True
        user.email_verification_token = None
        user.save()
        
        return HttpResponse("Email verified! You can now log in.")
    
class DeleteAccountView(LoginRequiredMixin,DeleteView):
    model = User
    template_name = 'research_repo/account_removal.html'
    success_url = reverse_lazy('/')

    def get_object(self, queryset = None):
        return self.request.user
        

class PublicationListView(LoginRequiredMixin, ListView):
    model = Publication
    template_name = 'research_repo/publication_list.html'
    context_object_name = 'publications'

    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get('q', '').strip()

        # 🔐 Base RBAC filter
        queryset = Publication.objects.filter(
            Q(is_public=True) |
            Q(grants__viewer=user,
              grants__access_granted=True,
              grants__expires_at__gt=timezone.now()) |
            Q(uploader=user) |
            Q(authors__user=user)
        ).distinct()

        # 🔍 Search layer
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(abstract__icontains=query)
            )

        return queryset

class PublicationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Publication
    template_name = 'research_repo/publication_detail.html'
    context_object_name = 'publication'

    def test_func(self):
        publication = self.get_object()
        user = self.request.user
        
        if publication.is_public:
            return True

        if (publication.uploader == user or 
            publication.authors.filter(user=user).exists() or 
            publication.grants.filter(
                viewer=user, 
                access_granted=True, 
                expires_at__gt=timezone.now()
            ).exists()):
            return True

        if publication.auto_approve_access and user.is_authenticated and user.can_upload():
            return True

        return False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        publication = self.object
        user = self.request.user
        
        is_verified_faculty = user.is_authenticated and user.can_upload()
        
        context['can_view_pdf'] = (
            user.is_superuser or
            publication.is_public or
            publication.uploader == user or
            publication.authors.filter(user=user).exists() or
            publication.grants.filter(
                viewer=user, 
                access_granted=True, 
                expires_at__gt=timezone.now()
            ).exists() or
            (publication.auto_approve_access and is_verified_faculty)
        )
        return context
    
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
    template_name = 'upload_document.html'
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
    
class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'research_repo/settings.html'
    
    def post(self, request, *args, **kwargs):
        # Handle Faculty Verification Submission
        if 'verify_submit' in request.POST:
            id_doc = request.FILES.get('id_document')
            if id_doc:
                request.user.id_document = id_doc
                request.user.save()
                messages.success(request, "ID document uploaded successfully. Waiting for admin approval.")
            else:
                messages.error(request, "Please select an ID file to upload.")
                
        # Handle Profile Save (if you have logic for this)
        elif 'profile_save' in request.POST:
            # Your existing profile update logic
            pass
            
        return redirect('settings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # You can add extra context here if needed
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'research_repo/profile.html'

class DashboardView(LoginRequiredMixin, DetailView):
    model = Publication
    template_name = 'dashboard.html'
    context_object_name = 'publication'

class DiscoveryView(TemplateView):
    template_name = 'research_repo/discovery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['public_publications'] = Publication.objects.filter(is_public=True).select_related('uploader').prefetch_related('authors')
        return context