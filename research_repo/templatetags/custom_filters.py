"""
Custom template tags and filters for ScholarVault
Provides utility functions for:
- Text truncation and formatting
- Date/time formatting
- Access control display
- Publication status badges
- Author listing utilities
"""

from django import template
from django.utils.html import escape
from django.template.defaultfilters import stringformat
from datetime import datetime, timedelta

register = template.Library()


@register.filter
def truncate_words(text, num_words=50):
    """
    Truncate text to a specified number of words and add ellipsis.
    
    Usage: {{ publication.abstract|truncate_words:30 }}
    """
    if not text:
        return ""
    
    words = text.split()
    if len(words) <= num_words:
        return text
    
    return " ".join(words[:num_words]) + "..."


@register.filter
def format_date(date_obj):
    """
    Format date in a readable format.
    
    Usage: {{ publication.created_at|format_date }}
    """
    if not date_obj:
        return "N/A"
    
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        except:
            return date_obj
    
    today = datetime.now().date() if hasattr(datetime.now(), 'date') else datetime.now()
    if isinstance(date_obj, datetime):
        date_obj = date_obj.date()
    
    if date_obj == today:
        return "Today"
    elif date_obj == today - timedelta(days=1):
        return "Yesterday"
    elif date_obj > today - timedelta(days=7):
        days_ago = (today - date_obj).days
        return f"{days_ago} days ago"
    
    return date_obj.strftime("%b %d, %Y")


@register.filter
def author_names(authors, limit=3):
    """
    Format a list of authors as a comma-separated string with limit.
    
    Usage: {{ publication.authors.all|author_names:5 }}
    """
    author_list = list(authors)
    
    if len(author_list) <= limit:
        return ", ".join([a.user.username for a in author_list])
    
    names = [a.user.username for a in author_list[:limit]]
    remaining = len(author_list) - limit
    return f"{', '.join(names)} and {remaining} more"


@register.filter
def access_status_badge(publication, user):
    """
    Generate an access status badge based on publication and user.
    
    Usage: {{ publication|access_status_badge:user }}
    """
    if not user or user.is_anonymous:
        return '<span class="badge bg-secondary"><i class="bi bi-lock"></i> Public Only</span>'
    
    if publication.is_public:
        return '<span class="badge bg-success"><i class="bi bi-globe"></i> Public</span>'
    
    if publication.uploader == user or publication.authors.filter(user=user).exists():
        return '<span class="badge bg-primary"><i class="bi bi-person-check"></i> Owner</span>'
    
    # Check for active access grant
    from django.utils import timezone
    has_access = publication.grants.filter(
        viewer=user,
        access_granted=True,
        expires_at__gt=timezone.now()
    ).exists()
    
    if has_access:
        return '<span class="badge bg-info"><i class="bi bi-check-circle"></i> Granted Access</span>'
    
    return '<span class="badge bg-danger"><i class="bi bi-lock"></i> No Access</span>'


@register.filter
def publication_status_display(publication):
    """
    Display publication status as a formatted badge.
    
    Usage: {{ publication|publication_status_display }}
    """
    status = []
    
    if publication.is_public:
        status.append('<span class="badge bg-success"><i class="bi bi-globe"></i> Public</span>')
    else:
        status.append('<span class="badge bg-warning"><i class="bi bi-lock"></i> Private</span>')
    
    if publication.auto_approve_access:
        status.append('<span class="badge bg-info"><i class="bi bi-check-circle"></i> Auto-Approve</span>')
    
    return " ".join(status)


@register.filter
def can_edit_publication(publication, user):
    """
    Check if user can edit the publication.
    
    Usage: {% if publication|can_edit_publication:user %}...{% endif %}
    """
    if not user or user.is_anonymous:
        return False
    
    return (
        publication.uploader == user or
        publication.authors.filter(user=user).exists() or
        user.is_superuser
    )


@register.filter
def can_grant_access(publication, user):
    """
    Check if user can grant access to the publication.
    
    Usage: {% if publication|can_grant_access:user %}...{% endif %}
    """
    if not user or user.is_anonymous:
        return False
    
    return (
        publication.uploader == user or
        publication.authors.filter(user=user).exists() or
        user.is_superuser
    )


@register.filter
def has_pdf(publication):
    """
    Check if publication has a PDF attached.
    
    Usage: {% if publication|has_pdf %}...{% endif %}
    """
    return publication.full_pdf and publication.full_pdf.url


@register.filter
def user_contribution_role(authors_queryset, user):
    """
    Get the contribution role of a specific user in a publication.
    
    Usage: {{ publication.authors.all|user_contribution_role:request.user }}
    """
    authorship = authors_queryset.filter(user=user).first()
    if authorship:
        return authorship.contribution_role
    return "Unknown"


@register.filter
def truncate_chars_smart(text, max_chars=150):
    """
    Truncate text to max characters, breaking at word boundaries.
    
    Usage: {{ publication.title|truncate_chars_smart:100 }}
    """
    if not text or len(text) <= max_chars:
        return text
    
    truncated = text[:max_chars].rsplit(' ', 1)[0]
    return truncated + "..."


@register.filter
def days_ago(date_obj):
    """
    Calculate days between date and today.
    
    Usage: {{ publication.created_at|days_ago }}
    """
    if not date_obj:
        return "Unknown"
    
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        except:
            return date_obj
    
    if isinstance(date_obj, datetime):
        date_obj = date_obj.date()
    
    today = datetime.now().date()
    delta = today - date_obj
    
    if delta.days == 0:
        return "today"
    elif delta.days == 1:
        return "yesterday"
    elif delta.days < 7:
        return f"{delta.days} days ago"
    elif delta.days < 30:
        weeks = delta.days // 7
        return f"{weeks} week{'s' if weeks > 1 else ''} ago"
    elif delta.days < 365:
        months = delta.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    else:
        years = delta.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"


@register.simple_tag
def user_publication_count(user):
    """
    Get the total publication count for a user.
    
    Usage: {% user_publication_count user %}
    """
    from research_repo.models import Publication
    return Publication.objects.filter(uploader=user).count()


@register.simple_tag
def user_coauthorship_count(user):
    """
    Get the total co-authorship count for a user.
    
    Usage: {% user_coauthorship_count user %}
    """
    from research_repo.models import Authorship
    return Authorship.objects.filter(user=user).count()


@register.inclusion_tag('research_repo/tags/publication_card.html')
def publication_card(publication, user=None):
    """
    Render a publication card component.
    
    Usage: {% publication_card publication user %}
    """
    can_edit = False
    can_grant = False
    
    if user and not user.is_anonymous:
        can_edit = (
            publication.uploader == user or
            publication.authors.filter(user=user).exists()
        )
        can_grant = can_edit
    
    return {
        'publication': publication,
        'user': user,
        'can_edit': can_edit,
        'can_grant': can_grant,
    }


# Safeguard for safe HTML rendering
register.filter('access_status_badge', access_status_badge)
register.filter('publication_status_display', publication_status_display)
