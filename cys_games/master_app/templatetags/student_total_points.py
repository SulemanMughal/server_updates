from django import template
from master_app.models import *
from master_app.views import customPrint
from django.db.models import Sum
from django.db.models import Q


register = template.Library()
@register.simple_tag
def student_total_points(student_id, *args, **kwargs):
    try:
        # TODO  :   Retrieve All courses for this student
        courses = AssignedStudents.objects.filter(Q(student__id = student_id))

        # TODO  :   Total Points
        points = 0

        # TODO : Retrieve Total Obtained points by Student
        for course in courses:        
            points = NetworkFlagSubmission.objects.filter(
                Q(student__id = course.id) & Q(status = "SUBMITTED")
            ).aggregate(Sum("obtainedPoints"))['obtainedPoints__sum']
        if points:
            return points
        return 0
    except Exception as e:
        customPrint(e)
        return 0