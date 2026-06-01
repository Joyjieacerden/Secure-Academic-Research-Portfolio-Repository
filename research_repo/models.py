from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('FACULTY', 'Faculty'),
        ('PEER_REVIEWER', 'Peer Reviewer'),
        ('GUEST', 'Guest'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='GUEST')
    is_identity_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    def is_faculty_verified(self):
        return self.role == 'FACULTY' and self.is_identity_verified
    
    def can_review(self):
        return self.role == 'PEER_REVIEWER' and self.is_identity_verified

    def can_access_document(self, publication):
        """Used by views to check if user can read a specific PDF."""
        if self.is_faculty_verified() and publication.portfolio.user == self:
            return True
        
        # Check for active assignment
        return self.reviewerassignment_set.filter(
            publication=publication, 
            expires_at__gt=timezone.now()
        ).exists()


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_description = models.CharField(max_length=50, help_text="e.g., Student, Faculty, Other")
    id_document_url = models.URLField(blank=True, null=True, help_text="URL to uploaded ID")
    
    def __str__(self):
        return f"Portfolio: {self.user.username} ({self.user_description})"


class Publication(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    full_pdf_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ReviewerAssignment(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    expires_at = models.DateTimeField()
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reviewer {self.reviewer.username} for {self.publication.title}"
    
    def is_active(self):
        return self.expires_at > timezone.now()