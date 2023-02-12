from django import template
from master_app.models import *
from master_app.views import customPrint
from django.db.models import Sum
from django.db.models import Q


register = template.Library()
@register.simple_tag
def student_course_points(student_id, *args, **kwargs):
    try:
        # TODO  :   Retrieve All submissions for a course by this AssignedStudents ID
        submissions = NetworkFlagSubmission.objects.filter(
            student__id = student_id
        )
        # print(submissions)
        points = 0
        if submissions.count():
            for i in submissions:
                points = points + i.obtainedPoints
        return points 
    except Exception as e:
        customPrint(e)
        return 0