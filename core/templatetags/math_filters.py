# store/templatetags/math_filters.py
from django import template

register = template.Library()

@register.filter
def add(value, arg):
    """Adds the arg to the value."""
    return value + arg

@register.filter
def subtract(value, arg):
    """Subtracts the arg from the value."""
    return value - arg

@register.filter
def mul(value, arg):
    """Multiplies the value by the arg."""
    return value * arg

@register.filter
def divide(value, arg):
    """Divides the value by the arg."""
    if arg == 0:
        return 0  # Avoid division by zero
    return value / arg
