# Built-in
from django.db import models
from django.contrib.auth import get_user_model

from django.utils import timezone
User = get_user_model()

from ckeditor.fields import RichTextField


from django.core.exceptions import ValidationError

from .choices import OPERATING_SYSTEM_CHOICES,  SCENARIOS_CATEGORYIES, RATING_CHOICES


# Create your models here.

# # Customized User
# class User(AbstractUser):
#     is_student = models.BooleanField(default=False)
#     is_teacher = models.BooleanField(default=False)

APPROVED_CHOICES = (
    ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Rejected", "Rejected")
)


class Course(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=False, default=timezone.now)
    end_time = models.DateTimeField(auto_now_add=False, default=timezone.now)
    created_timestamp = models.DateTimeField( auto_now_add=True )
    description = RichTextField()
    is_approved = models.CharField(max_length=10, choices=APPROVED_CHOICES, default="Pending")
    


    def __str__(self):
        return self.name


class AssignedStudents(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField( auto_now_add=True)


    def __str__(self):
        return "{course} - {student}".format(
            course = self.course.name,
            student = self.student.email
        )

    def clean(self):
        if not self.student.is_student :
            raise ValidationError("Only Students are allowed to added.")

    class Meta:
        unique_together = ('course', 'student')



class VirtualNetwork(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = RichTextField()
    operating_system = models.CharField(max_length=3, default=1 , choices=OPERATING_SYSTEM_CHOICES)
    scenarios = models.CharField(max_length=50, default=1 , choices=SCENARIOS_CATEGORYIES)
    rating  = models.CharField(max_length=1 , default=1, choices=RATING_CHOICES)
    ip_address = models.GenericIPAddressField(blank=True, null=True)


    def __str__(self):
        return self.name
