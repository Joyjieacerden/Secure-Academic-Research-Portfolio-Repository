from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from research_repo.models import User, Publication, Authorship

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(
        write_only=True, 
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise serializers.ValidationError(
                    "Invalid credentials. Please try again."
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    "This account has been deactivated."
                )
        else:
            raise serializers.ValidationError(
                "Both username and password are required."
            )

        attrs['user'] = user
        return attrs
    

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError(
                {"refresh": "Token is invalid or already expired."}
            )


class UserSerializer(serializers.ModelSerializer):
    can_upload = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'is_faculty', 
            'is_identity_verified', 'verified_at', 'verified_by', 
            'description', 'id_document_url', 'can_upload'
        ]
        read_only_fields = ['is_identity_verified', 'verified_at', 'verified_by']


class AuthorshipSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Authorship
        fields = ['id', 'user', 'user_username', 'publication', 'contribution_role']


class PublicationSerializer(serializers.ModelSerializer):
    authors = AuthorshipSerializer(many=True, read_only=True)
    uploader_username = serializers.CharField(source='uploader.username', read_only=True)

    class Meta:
        model = Publication
        fields = [
            'id', 'title', 'abstract', 'full_pdf_url', 
            'is_public', 'auto_approve_access', 'uploader', 
            'uploader_username', 'authors'
        ]
        read_only_fields = ['uploader']

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        request = context.get('request', None)
        
        super().__init__(*args, **kwargs)

        # Apply Column-Level Security Logic
        if request:
            user = request.user
            
            # Identify if we are inspecting a single object instance vs a list/queryset
            if self.instance and not isinstance(self.instance, (list, tuple, tuple.__class__)):
                publications = [self.instance]
            else:
                publications = []

            # Determine Premium / Reviewer status using built-in Django Group memberships
            is_premium_or_reviewer = False
            if user and user.is_authenticated:
                is_premium_or_reviewer = (
                    user.is_superuser or 
                    user.is_faculty or 
                    user.groups.filter(name__in=['Reviewers', 'Premium Engines']).exists()
                )

            # If the consumer is basic or unauthenticated, audit column protection
            if not is_premium_or_reviewer:
                # If a specific publication is being analyzed, honor custom AccessGrant/Owner methods
                if publications and user and user.is_authenticated:
                    pub = publications[0]
                    if user.has_access_to(pub):
                        return  # Granted! Do not pop the field.

                # Redact PDF link entirely for standard engines/public users
                self.fields.pop('full_pdf_url', None)