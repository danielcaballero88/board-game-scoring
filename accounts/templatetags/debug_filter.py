from django import template
from django.forms.boundfield import BoundField

register = template.Library()


@register.filter("debug_filter")
def debug_filter(element: BoundField) -> BoundField:
    """Dummy filter for debugging.

    Usage: put a breakpoint inside this filter and use it in a template
    by doing:
        {% load debug_filter %}
        {% form.field | dummy %}
    """
    breakpoint()
    return element
