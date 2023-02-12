from django import template
from master_app.models import *
from master_app.views import customPrint
# from django.db.models import Sum
from django.db.models import Q


register = template.Library()
@register.simple_tag
def student_course_flag_resolved(student_id, *args, **kwargs):
    try:

        # TODO  :   Total Flag resolved for this course
        submissions = NetworkFlagSubmission.objects.filter(
            student__id = student_id,
            status = "SUBMITTED"
        ).count()

        return submissions
    except Exception as e:
        customPrint(e)
        return 0