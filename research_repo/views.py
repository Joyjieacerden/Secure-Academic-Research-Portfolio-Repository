from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, PortfolioForm, PublicationForm,LoginForm
from .models import User, Portfolio, Publication, Authorship, AccessGrant
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView,TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin,PermissionRequiredMixin
from cloudinary.uploader import upload



# Create your views here.

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'research_repo/register.html'
    success_url = '/login/'

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response
    
class UserLoginView(LoginView):
    template_name = 'research_repo/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().form_valid(form)
    
class PortfolioCreateView(LoginRequiredMixin, CreateView,PermissionRequiredMixin,UserPassesTestMixin):
    model = Portfolio
    form_class = PortfolioForm
    template_name = 'research_repo/portfolio_form.html'
    success_url = '/'
    permission_required = 'research_repo.add_portfolio'


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['FACULTY']
    
class PortfolioDetailView(LoginRequiredMixin, DetailView,UserPassesTestMixin):
    model = Portfolio
    template_name = 'research_repo/portfolio_detail.html'
    context_object_name = 'portfolio'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['FACULTY']
    
class PortfolioListView(LoginRequiredMixin, ListView,UserPassesTestMixin):
    model = Portfolio
    template_name = 'research_repo/portfolio_list.html'
    context_object_name = 'portfolios'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['FACULTY']
    
class PortfolioUpdateView(LoginRequiredMixin, UpdateView,PermissionRequiredMixin,UserPassesTestMixin):
    model = Portfolio
    form_class = PortfolioForm
    template_name = 'research_repo/portfolio_form.html'
    success_url = '/'
    permission_required = 'research_repo.change_portfolio'

    def test_func(self):
        portfolio = self.get_object()
        return self.request.user.is_authenticated and self.request.user == portfolio.user and self.request.user.role in ['FACULTY']
    
class PortfolioDeleteView(LoginRequiredMixin, DeleteView,PermissionRequiredMixin,UserPassesTestMixin):
    model = Portfolio
    success_url = '/'
    permission_required = 'research_repo.delete_portfolio'

    def test_func(self):
        portfolio = self.get_object()
        return self.request.user.is_authenticated and self.request.user == portfolio.user and self.request.user.role in ['FACULTY']
    
class PublicationCreateView(LoginRequiredMixin, CreateView,PermissionRequiredMixin,UserPassesTestMixin):
    model = Publication
    form_class = PublicationForm
    template_name = 'research_repo/publication_form.html'
    success_url = '/'
    permission_required = 'research_repo.add_publication'

    def form_valid(self, form):
       pdf_file = self.request.FILES.get('full_pdf')

       if pdf_file:
            result = upload(pdf_file,resource_type='raw', folder='publications/')
            form.instance.full_pdf_url = result['secure_url']
        
       form.instance.uploader = self.request.user 
       return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['FACULTY']
    
class PublicationDetailView(DetailView):
    model = Publication
    template_name = 'research_repo/publication_detail.html'
    context_object_name = 'publication'

class PublicationListView(ListView):
    model = Publication
    template_name = 'research_repo/publication_list.html'
    context_object_name = 'publications'
    paginate_by = 10

class PublicationUpdateView(LoginRequiredMixin, UpdateView,PermissionRequiredMixin,UserPassesTestMixin):
    model = Publication
    form_class = PublicationForm
    template_name = 'research_repo/publication_form.html'
    success_url = '/'
    permission_required = 'research_repo.change_publication'

    def form_valid(self, form):
       pdf_file = self.request.FILES.get('full_pdf')

       if pdf_file:
            result = upload(pdf_file,resource_type='raw', folder='publications/')
            form.instance.full_pdf_url = result['secure_url']
        
       return super().form_valid(form)

    def test_func(self):
        publication = self.get_object()
        return self.request.user.is_authenticated and self.request.user.can_modify_publication(publication)
    
class PublicationDeleteView(LoginRequiredMixin, DeleteView,PermissionRequiredMixin,UserPassesTestMixin):
    model = Publication
    success_url = '/'
    permission_required = 'research_repo.delete_publication'

    def test_func(self):
        publication = self.get_object()
        return self.request.user.is_authenticated and self.request.user.role in ['FACULTY']
    
class DashboardView(LoginRequiredMixin, ListView,UserPassesTestMixin):
    model = Publication
    template_name = 'research_repo/dashboard.html'
    context_object_name = 'publications'

    def get_queryset(self):
        return Publication.objects.filter(authorship__author=self.request.user).distinct()   

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['FACULTY'] 
    
class SetitngsView(LoginRequiredMixin, TemplateView):
    template_name = 'research_repo/settings.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['FACULTY']
    


    

    


    

    





