import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def highlight(text, query):
    if not query or not text:
        return text
    
    # Case-insensitive replacement wrapping matches in a styled span
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    highlighted = pattern.sub(
        lambda match: f'<mark class="bg-amber-200 text-amber-900 font-semibold px-0.5 rounded">{match.group(0)}</mark>',
        str(text)
    )
    return mark_safe(highlighted)