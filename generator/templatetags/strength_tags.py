from django import template

register = template.Library()

@register.filter
def get_strength_color(score):
    """Returns a Bootstrap color class based on password strength score."""
    colors = ['danger', 'danger', 'warning', 'info', 'success']
    return colors[score]

@register.filter
def get_strength_text(score):
    """Returns a text description based on password strength score."""
    labels = ['Very Weak', 'Weak', 'Moderate', 'Strong', 'Very Strong']
    return labels[score]