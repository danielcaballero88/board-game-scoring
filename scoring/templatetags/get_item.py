from django import template
from django.forms.boundfield import BoundField

register = template.Library()


@register.filter("get_item")
def get_item(value, arg) -> BoundField:
    """Custom filter to get a value from a dictionary

    Usage:
        {% load get_item %}
        {% some_dict|get_item:key %}
    """
    return value.get(arg)
