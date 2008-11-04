from django.template import Library
from django.conf import settings
from django.utils.safestring import mark_safe

register = Library()

@register.filter
def wikify(value):
    """Makes WikiWords"""
    import re
    wikifier = re.compile(r'\b(([A-Z]+[a-z]+){2,})\b')
    return mark_safe( wikifier.sub(r'<a href="%s\1/">\1</a>'%settings.WIKI_SITEBASE, value) )
