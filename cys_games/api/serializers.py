from rest_framework import serializers
from master_app.models import Course


class CourseSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Course 
        fields = ('name',)