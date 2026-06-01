from django.forms import ModelForm,InlineFormSet
from django.contrib.auth.forms import UserCreationForm
from .models import User, Portfolio, Publication,ReviewerAssignment


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = ['user_description', 'id_document']

class PublicationForm(ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'abstract', 'full_pdf_url']

class ReviewerAssignmentForm(ModelForm):
    class Meta:
        model = ReviewerAssignment
        fields = ['publication', 'reviewer', 'expires_at']

