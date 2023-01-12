from django import template
from master_app.models import NetworkFlagSubmission, AssignedStudents, Course, NetworkFlag
from master_app.views import customPrint
register = template.Library()
@register.filter
def flag_sub_status(flag_id, user_id , *args, **kwargs):
    try:
        # customPrint(flag_id)
        netFlag = NetworkFlag.objects.get(
            id = flag_id
        )
        student = AssignedStudents.objects.get(
            course = netFlag.course,
            student__id = user_id
        )
        if NetworkFlagSubmission.objects.filter(
            flag_id = netFlag.flag_id,
            student = student,
            status= "SUBMITTED"
        ).count():
            return 1
        return None
    except Exception as e:
        return None