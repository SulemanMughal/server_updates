from django import template
from master_app.models import  *
from master_app.views import customPrint
register = template.Library()
@register.simple_tag
def count_course_status(course_status , *args, **kwargs):
    try:
        return Course.objects.filter(is_approved = course_status).count()
    except Exception as e:
        customPrint(e)
        return 0