from django.contrib import admin

from .models import Course, AssignedStudents

# Register your models here.


# admin.site.register(Course)
class AssignedStudentInline(admin.TabularInline):
    model = AssignedStudents

class CourseAdmin(admin.ModelAdmin):
    inlines = [
        AssignedStudentInline
    ]


admin.site.register(Course, CourseAdmin)