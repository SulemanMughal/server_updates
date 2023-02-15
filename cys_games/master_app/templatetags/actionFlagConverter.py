from django import template
register = template.Library()

ACTION_FLAGS = {
    "1": "ADDITION",
    "2": "CHANGED",
    "3": "DELETION"
}


@register.filter
def actionFlagConverter(value):
    return ACTION_FLAGS[str(value)]
