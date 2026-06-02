from django.forms import ModelForm,inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import AccessGrant, User, Portfolio, Publication,Authorship


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
        fields = ['user_description', 'id_document_url']

class PublicationForm(inlineformset_factory( Publication, Authorship, fields=['contribution_role'], extra=1)):
    class Meta:
        model = Publication
        fields = ['title', 'abstract', 'full_pdf_url']



