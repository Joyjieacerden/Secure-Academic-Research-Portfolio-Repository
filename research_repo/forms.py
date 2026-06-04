from django.forms import ModelForm, ValidationError, Form
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Publication, User, AccessGrant, Authorship
from .validators import validate_institutional_email
import cloudinary.uploader



class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise ValidationError('Email address is required.')
        validate_institutional_email(email)
        # Uniqueness check — prevents duplicate accounts
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('An account with this email address already exists.')
        return email.lower()

class PublicationForm(ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'abstract', 'full_pdf_url', 'is_public', 'auto_approve_access']

class AuthorshipForm(ModelForm):
    class Meta:
        model = Authorship
        fields = ['user', 'contribution_role']

AuthorshipFormSet = inlineformset_factory(Publication, Authorship, form=AuthorshipForm, extra=1, can_delete=True)


class UploadDocumentForm(Form):
    class Meta:
        fields = ['title', 'abstract', 'full_pdf_url', 'is_public', 'auto_approve_access']

    def clean_full_pdf_url(self):
        file = self.cleaned_data.get('full_pdf_url')
        if file:
            try:
                result = cloudinary.uploader.upload(file)
                return result['secure_url']
            except Exception as e:
                raise ValidationError(f"File upload failed: {str(e)}")
        raise ValidationError("No file provided.")
    
class AccessGrantForm(ModelForm):
    class Meta:
        model = AccessGrant
        fields = ['viewer', 'access_granted', 'expires_at']