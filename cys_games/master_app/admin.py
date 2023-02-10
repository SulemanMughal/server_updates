from django.contrib import admin

from .models import Course, AssignedStudents, VirtualNetwork, CourseChallenge, ChallengeSubmission, NetworkFlag, NetworkFlagSubmission

# Register your models here.
import datetime
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE


# admin.site.register(Course)
class AssignedStudentInline(admin.TabularInline):
    model = AssignedStudents


class VirtualNetworkInline(admin.TabularInline):
    model = VirtualNetwork
    min_num = 1
    max_num = 1
    extra = 0

class CourseAdmin(admin.ModelAdmin):
    inlines = [
        AssignedStudentInline,
        VirtualNetworkInline
    ]
    list_display=[
        "name",
        "is_approved"
    ]


class VirtualNetworkAdmin(admin.ModelAdmin):
    list_display=[
        "name",
        "course",
        "operating_system",
        "scenarios"
    ]

class NetworkFlagSubmissionAdmin(admin.ModelAdmin):
    list_display=[
        'student',
        'flag_id',
        'attemptUsed',
        'status',
        'obtainedPoints',
    ]


class NetworkFlagAdmin(admin.ModelAdmin):
    list_display=[
        "course",
        "flag_id",
        "points",
        "original_answer",
        "imageRef"
    ]





class MoniterLog(admin.ModelAdmin):
    list_display = ('action_time','user','content_type','object_repr','change_message','action_flag')
    list_filter = ['action_time','user','content_type']
    ordering = ('-action_time',)


admin.site.register(Course, CourseAdmin)
admin.site.register(VirtualNetwork, VirtualNetworkAdmin)
admin.site.register(CourseChallenge)
admin.site.register(ChallengeSubmission)
admin.site.register(NetworkFlag, NetworkFlagAdmin)
admin.site.register(NetworkFlagSubmission, NetworkFlagSubmissionAdmin)
admin.site.register(LogEntry,MoniterLog)
admin.site.register(AssignedStudents)