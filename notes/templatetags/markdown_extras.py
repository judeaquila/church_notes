from django import template
from django.utils.safestring import mark_safe
import markdown as md

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    if not text:
        return ""
    
    # Standard extensions for code highlighting, tables, and auto-linking
    extensions = [
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        'markdown.extensions.nl2br',
        'markdown.extensions.sane_lists',
    ]
    
    html = md.markdown(text, extensions=extensions)
    return mark_safe(html)