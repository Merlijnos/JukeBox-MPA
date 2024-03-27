from django import template

register = template.Library()

@register.filter
def to_minutes(value):
    minutes = value // 60000
    seconds = round((value % 60000) / 1000)
    return f"{minutes}:{seconds:02}"
