from django.contrib import admin

from .models import Course, AssignedStudents, VirtualNetwork, CourseChallenge

# Register your models here.


# admin.site.register(Course)
class AssignedStudentInline(admin.TabularInline):
    model = AssignedStudents

class CourseAdmin(admin.ModelAdmin):
    inlines = [
        AssignedStudentInline
    ]


admin.site.register(Course, CourseAdmin)

admin.site.register(VirtualNetwork)
admin.site.register(CourseChallenge)