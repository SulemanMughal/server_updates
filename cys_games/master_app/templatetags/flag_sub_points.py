from django import template
from master_app.models import NetworkFlagSubmission, AssignedStudents, Course, NetworkFlag
from master_app.views import customPrint
register = template.Library()
@register.simple_tag
def flag_sub_points(flag_id, user_id , *args, **kwargs):
    try:
        # customPrint(flag_id)
        netFlag = NetworkFlag.objects.get(
            id = flag_id
        )
        student = AssignedStudents.objects.get(
            course = netFlag.course,
            student__id = user_id
        )
        # if NetworkFlagSubmission.objects.filter(
        #     flag_id = netFlag.flag_id,
        #     student = student,
        #     status= "SUBMITTED"
        # ).count():
        #     return 1
        # customPrint(NetworkFlagSubmission.objects.filter(
        #     flag_id = netFlag.flag_id,
        #     student = student,
        #     status= "SUBMITTED"
        # ).obtainedPoints)
        return NetworkFlagSubmission.objects.get(
            flag_id = netFlag.flag_id,
            student = student,
            status= "SUBMITTED"
        ).obtainedPoints
        
    except Exception as e:
        customPrint(e)
        return 0