from django.contrib import admin

from .models import Course, AssignedStudents, VirtualNetwork, CourseChallenge, ChallengeSubmission, NetworkFlag, NetworkFlagSubmission

# Register your models here.


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


admin.site.register(Course, CourseAdmin)

admin.site.register(VirtualNetwork)
admin.site.register(CourseChallenge)
admin.site.register(ChallengeSubmission)
admin.site.register(NetworkFlag)
admin.site.register(NetworkFlagSubmission)