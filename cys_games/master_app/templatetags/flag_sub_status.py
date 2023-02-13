from django import template
from master_app.models import NetworkFlagSubmission, AssignedStudents, Course, NetworkFlag
from master_app.views import customPrint
register = template.Library()


@register.filter
def flag_sub_status(flag_id,  *args, **kwargs):
    try:
        # netFlag = NetworkFlag.objects.get(
        #     id=flag_id
        # )
        # student = AssignedStudents.objects.get(
        #     course=netFlag.course,
        #     student__id=user_id
        # )
        submission = NetworkFlagSubmission.objects.get(
            id=flag_id
        )
        if submission.status == "SUBMITTED":
            return True
        return None
    except Exception as e:
        return None
