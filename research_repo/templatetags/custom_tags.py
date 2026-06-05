from django import template
from django.utils.html import format_html
from datetime import datetime

register = template.Library()

# ============================================================================
# PUBLICATION CARD TAG
# ============================================================================

@register.inclusion_tag('research_repo/tags/publication_card.html')
def publication_card(publication, show_actions=True):
    """
    Render a publication card with all details
    
    Usage: {% publication_card publication show_actions=True %}
    """
    return {
        'publication': publication,
        'show_actions': show_actions,
        'pub_date': publication.publication_date.strftime('%b %d, %Y') if publication.publication_date else 'Not set',
        'author_count': publication.authors.count(),
    }


# ============================================================================
# STATUS INDICATOR TAG
# ============================================================================

@register.simple_tag
def status_indicator(is_public, show_label=True):
    """
    Render status indicator with color
    
    Usage: {% status_indicator publication.is_public %}
    """
    if is_public:
        badge_class = 'badge-published'
        label = 'Published'
        color = '#27ae60'
    else:
        badge_class = 'badge-draft'
        label = 'Draft'
        color = '#f39c12'
    
    indicator = f'<span class="badge {badge_class}" style="background-color: {color}15; color: {color};">'
    if show_label:
        indicator += f'<i class="bi bi-{"check-circle" if is_public else "pencil"}"></i> {label}'
    else:
        indicator += '<i class="bi bi-circle-fill" style="font-size: 0.5rem;"></i>'
    indicator += '</span>'
    
    return format_html(indicator)


# ============================================================================
# ACCESS GRANT INFO TAG
# ============================================================================

@register.simple_tag
def access_expiry_label(access_grant):
    """
    Render access expiry information
    
    Usage: {% access_expiry_label access_grant %}
    """
    if not access_grant or not access_grant.access_granted:
        return format_html('<span class="text-muted"><i class="bi bi-lock"></i> No access</span>')
    
    expires_at = access_grant.expires_at
    now = datetime.now().replace(tzinfo=expires_at.tzinfo) if expires_at.tzinfo else datetime.now()
    
    if expires_at <= now:
        return format_html(
            '<span style="color: #e74c3c;"><i class="bi bi-exclamation-circle"></i> Expired on {}</span>',
            expires_at.strftime('%b %d, %Y')
        )
    
    days_left = (expires_at.date() - now.date()).days
    if days_left <= 7:
        return format_html(
            '<span style="color: #f39c12;"><i class="bi bi-clock"></i> Expires in {} days</span>',
            days_left
        )
    
    return format_html(
        '<span style="color: #27ae60;"><i class="bi bi-check-circle"></i> Expires on {}</span>',
        expires_at.strftime('%b %d, %Y')
    )


# ============================================================================
# AUTHOR LIST TAG
# ============================================================================

@register.simple_tag
def author_list(publication, limit=3):
    """
    Render list of authors with optional limit
    
    Usage: {% author_list publication limit=3 %}
    """
    authors = publication.authors.all()[:limit]
    
    if not authors:
        return format_html('<em class="text-muted">No authors listed</em>')
    
    author_html = '<div class="author-list" style="font-size: 0.9rem;">'
    
    for author in authors:
        name = author.user.get_full_name() or author.user.username
        role = author.contribution_role or 'Contributor'
        author_html += f'<div class="author-item"><strong>{name}</strong> <span style="color: #95a5a6;">({role})</span></div>'
    
    if publication.authors.count() > limit:
        remaining = publication.authors.count() - limit
        author_html += f'<div class="author-item text-muted"><em>+ {remaining} more</em></div>'
    
    author_html += '</div>'
    
    return format_html(author_html)


# ============================================================================
# FILTER BADGE TAG
# ============================================================================

@register.simple_tag
def filter_badge(filter_name, filter_value):
    """
    Render a filter badge
    
    Usage: {% filter_badge "Status" "Published" %}
    """
    return format_html(
        '<span style="background: rgba(139, 0, 0, 0.1); color: #8B0000; padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600; display: inline-block; margin-right: 0.5rem;">{}: <strong>{}</strong></span>',
        filter_name,
        filter_value
    )


# ============================================================================
# STATS CARD TAG
# ============================================================================

@register.inclusion_tag('research_repo/tags/stats_card.html')
def stats_card(label, value, icon, color='purple', clickable=False, link='#'):
    """
    Render a stats card
    
    Usage: {% stats_card "Total Publications" 42 "bi-journals" "purple" %}
    """
    color_map = {
        'purple': '#8B0000',
        'pink': '#ec407a',
        'cyan': '#29b6f6',
        'green': '#27ae60',
    }
    
    return {
        'label': label,
        'value': value,
        'icon': icon,
        'color': color_map.get(color, '#8B0000'),
        'clickable': clickable,
        'link': link,
    }


# ============================================================================
# EMPTY STATE TAG
# ============================================================================

@register.simple_tag
def empty_state(message, icon='inbox', action_link=None, action_text=None):
    """
    Render empty state message
    
    Usage: {% empty_state "No publications found" "inbox" %}
    """
    html = f'<div class="empty-state" style="text-align: center; padding: 4rem 2rem;">'
    html += f'<i class="bi bi-{icon}" style="font-size: 4.5rem; color: #ddd; display: block; margin-bottom: 1.5rem;"></i>'
    html += f'<h4 style="color: #2c3e50; margin-bottom: 0.75rem;">{message}</h4>'
    
    if action_link and action_text:
        html += f'<a href="{action_link}" style="color: #8B0000; text-decoration: none; font-weight: 700;">{action_text}</a>'
    
    html += '</div>'
    
    return format_html(html)


# ============================================================================
# PAGINATION INFO TAG
# ============================================================================

@register.simple_tag
def pagination_info(current_page, total_pages, total_items):
    """
    Render pagination information
    
    Usage: {% pagination_info page_num total_pages item_count %}
    """
    start_item = (current_page - 1) * 8 + 1
    end_item = min(current_page * 8, total_items)
    
    return format_html(
        'Showing <strong>{}</strong> to <strong>{}</strong> of <strong>{}</strong> items (Page <strong>{}</strong> of <strong>{}</strong>)',
        start_item,
        end_item,
        total_items,
        current_page,
        total_pages
    )
