from django import template
from master_app.models import *
# from master_app.views import customPrint
register = template.Library()
@register.simple_tag
def attacker_flag(course_id, student_id , *args, **kwargs):
    try:
        student = AssignedStudents.objects.get(
            course__id = course_id,
            student__id = student_id
        )
        if student.user_type == "1":
            return True
        return False
    except Exception as e:
        print(e)
        return False