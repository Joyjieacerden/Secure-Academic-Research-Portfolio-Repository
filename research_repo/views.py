from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, PortfolioForm, PublicationForm, ReviewerAssignmentForm,LoginForm
from .models import User, Portfolio, Publication, ReviewerAssignment
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin,PermissionRequiredMixin



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
        return self.request.user.is_authenticated and self.request.user.role in ['FACULTY', 'PEER_REVIEWER']
    
class PortfolioDetailView(LoginRequiredMixin, DetailView):
    model = Portfolio
    template_name = 'research_repo/portfolio_detail.html'
    context_object_name = 'portfolio'

    
    
    
        
