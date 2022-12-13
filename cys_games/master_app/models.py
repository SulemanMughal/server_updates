# Built-in
from django.db import models
from django.contrib.auth import get_user_model

from django.utils import timezone
User = get_user_model()

# Create your models here.

# # Customized User
# class User(AbstractUser):
#     is_student = models.BooleanField(default=False)
#     is_teacher = models.BooleanField(default=False)




class Course(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=False, default=timezone.now)
    end_time = models.DateTimeField(auto_now_add=False, default=timezone.now)


class AssignedStudents(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField( auto_now_add=True)