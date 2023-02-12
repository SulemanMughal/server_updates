from django import template
from master_app.models import *
from master_app.views import customPrint
# from django.db.models import Sum
from django.db.models import Q


register = template.Library()
@register.simple_tag
def student_total_flag_resolved(student_id, *args, **kwargs):
    try:

        # TODO  :   Retrieve All courses for this student
        courses = AssignedStudents.objects.filter(Q(student__id = student_id))

        # TODO  :   Total Submissions
        submissions = 0

        # TODO : Retrieve All Flag Submission by Student
        for course in courses:        
            submissions = submissions + NetworkFlagSubmission.objects.filter(Q(student__id = course.id) & Q(status="SUBMITTED")).count()
        return submissions
    except Exception as e:
        customPrint(e)
        return 0