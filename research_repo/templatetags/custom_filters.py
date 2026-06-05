from django import template
from django.utils.html import format_html
from datetime import datetime

register = template.Library()

# ============================================================================
# DATE FORMATTING FILTERS
# ============================================================================

@register.filter
def format_publication_date(date_value):
    """
    Format publication date as 'Mon DD, YYYY'
    If no date provided, returns 'Not set'
    
    Usage: {{ publication.publication_date|format_publication_date }}
    """
    if not date_value:
        return 'Not set'
    
    try:
        if isinstance(date_value, str):
            date_value = datetime.strptime(date_value, '%Y-%m-%d').date()
        return date_value.strftime('%b %d, %Y')
    except (ValueError, AttributeError):
        return 'Invalid date'


@register.filter
def format_created_date(datetime_value):
    """
    Format created_at datetime as 'Mon DD, YYYY at HH:MM'
    
    Usage: {{ publication.created_at|format_created_date }}
    """
    if not datetime_value:
        return 'Not available'
    
    try:
        return datetime_value.strftime('%b %d, %Y at %H:%M')
    except AttributeError:
        return 'Invalid date'


@register.filter
def days_since(date_value):
    """
    Return number of days since given date
    
    Usage: {{ publication.publication_date|days_since }} days ago
    """
    if not date_value:
        return 'unknown'
    
    try:
        if isinstance(date_value, str):
            date_value = datetime.strptime(date_value, '%Y-%m-%d').date()
        delta = datetime.now().date() - date_value
        return delta.days
    except (ValueError, AttributeError, TypeError):
        return 'unknown'


# ============================================================================
# STATUS & BADGE FILTERS
# ============================================================================

@register.filter
def status_badge(is_public):
    """
    Return HTML badge for publication status
    
    Usage: {{ publication.is_public|status_badge|safe }}
    """
    if is_public:
        return format_html(
            '<span class="badge" style="background-color: #d4edda; color: #1e5631; padding: 0.5rem 0.875rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">Published</span>'
        )
    else:
        return format_html(
            '<span class="badge" style="background-color: #fff3e0; color: #e65100; padding: 0.5rem 0.875rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">Draft</span>'
        )


@register.filter
def access_status_badge(access_granted):
    """
    Return HTML badge for access status
    
    Usage: {{ access_grant.access_granted|access_status_badge|safe }}
    """
    if access_granted:
        return format_html(
            '<span class="badge" style="background-color: #d4edda; color: #1e5631; padding: 0.4rem 0.75rem; border-radius: 15px; font-size: 0.75rem; font-weight: 600;"><i class="bi bi-check-circle"></i> Granted</span>'
        )
    else:
        return format_html(
            '<span class="badge" style="background-color: #f8d7da; color: #721c24; padding: 0.4rem 0.75rem; border-radius: 15px; font-size: 0.75rem; font-weight: 600;"><i class="bi bi-x-circle"></i> Pending</span>'
        )


# ============================================================================
# TEXT TRUNCATION FILTERS
# ============================================================================

@register.filter
def truncate_words(text, num_words=20):
    """
    Truncate text to specified number of words and add ellipsis
    
    Usage: {{ publication.abstract|truncate_words:30 }}
    """
    if not text:
        return ''
    
    words = text.split()
    if len(words) > num_words:
        return ' '.join(words[:num_words]) + '...'
    return text


@register.filter
def truncate_chars(text, num_chars=100):
    """
    Truncate text to specified number of characters and add ellipsis
    
    Usage: {{ publication.title|truncate_chars:50 }}
    """
    if not text:
        return ''
    
    if len(text) > num_chars:
        return text[:num_chars] + '...'
    return text


# ============================================================================
# LIST/ARRAY FILTERS
# ============================================================================

@register.filter
def join_authors(authors, separator=', '):
    """
    Join author names with separator
    
    Usage: {{ publication.authors.all|join_authors|safe }}
    """
    if not authors:
        return 'No authors'
    
    try:
        author_names = [f"{author.user.get_full_name() or author.user.username}" for author in authors]
        return separator.join(author_names)
    except (AttributeError, TypeError):
        return 'Invalid authors'


@register.filter
def author_roles(authors):
    """
    Format authors with their roles as HTML list
    
    Usage: {{ publication.authors.all|author_roles|safe }}
    """
    if not authors:
        return format_html('<em>No authors</em>')
    
    try:
        roles_html = '<ul style="margin: 0; padding-left: 1.5rem; font-size: 0.9rem;">'
        for author in authors:
            name = author.user.get_full_name() or author.user.username
            role = author.contribution_role or 'Contributor'
            roles_html += f'<li><strong>{name}</strong> - {role}</li>'
        roles_html += '</ul>'
        return format_html(roles_html)
    except (AttributeError, TypeError):
        return format_html('<em>Invalid authors</em>')


# ============================================================================
# UTILITY FILTERS
# ============================================================================

@register.filter
def pluralize_publications(count):
    """
    Pluralize 'publication' based on count
    
    Usage: {{ publications.count|pluralize_publications }}
    """
    if count == 1:
        return '1 publication'
    return f'{count} publications'


@register.filter
def format_file_size(size_bytes):
    """
    Format file size in human-readable format
    
    Usage: {{ document.file.size|format_file_size }}
    """
    if not size_bytes:
        return '0 B'
    
    try:
        size_bytes = int(size_bytes)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f'{size_bytes:.1f} {unit}'
            size_bytes /= 1024
        return f'{size_bytes:.1f} TB'
    except (ValueError, TypeError):
        return 'Unknown'


@register.filter
def is_recent(date_value, days=7):
    """
    Check if date is within last N days
    
    Usage: {% if publication.publication_date|is_recent:14 %}Recently published{% endif %}
    """
    if not date_value:
        return False
    
    try:
        if isinstance(date_value, str):
            date_value = datetime.strptime(date_value, '%Y-%m-%d').date()
        delta = datetime.now().date() - date_value
        return delta.days <= days
    except (ValueError, AttributeError, TypeError):
        return False


@register.filter
def initials(full_name):
    """
    Get initials from full name
    
    Usage: {{ user.get_full_name|initials }}
    """
    if not full_name:
        return '?'
    
    names = full_name.strip().split()
    if len(names) == 1:
        return names[0][0].upper()
    return (names[0][0] + names[-1][0]).upper()
