from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('FACULTY', 'Faculty'),
        ('VIEWER', 'Viewer'),
        ('GUEST', 'Guest'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='GUEST')
    is_email_verified = models.BooleanField(default=False)
    is_identity_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_verified_faculty(self):
        return self.role == 'FACULTY' and self.is_identity_verified 
    
    def can_modify_publication(self, publication):
        if not self.is_verified_faculty():
            return False
        
        return publication.uploader == self 
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    
class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio')
    user_description = models.Charield(max_length=500, blank=True)
    id_document_url = models.URLField(max_length=200)

    def __str__(self):
        return f"Portfolio of {self.user.username}"
    
class Publication(models.Model):
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    full_pdf_url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, ondelete=models.CASCADE, related_name='uploaded_publications')

    def __str__(self):
        return self.title

class Authorship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    contribution_role = models.CharField(max_field=50)

class AccessGrant(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='grants' )
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    expires_at = models.DateTimeField()
    access_granted = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)

    def is_currently_valid(self):
        return self.access_granted and self.expires_at > timezone.now()
    
    def __str__(self):
        status = "Granted" if self.access_granted else "Pending"
        return f"{self.viewer.username} access to {self.publication.title} - {status}"

    