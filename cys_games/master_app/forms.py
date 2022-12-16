from django import forms

from django.contrib.auth import get_user_model
User  = get_user_model()

from .models import Course, AssignedStudents, VirtualNetwork, CourseChallenge


# ? User Login Form
class loginForm(forms.Form):
    email = forms.EmailField(label='Email Address', widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


# ? Course Create Form
class CreateCourseForm(forms.ModelForm):
    # name = forms.CharField()
    # start_time = forms.DateTimeField()
    # end_time = forms.DateTimeField()
    class Meta:
        model = Course
        fields  = [
            "name",
            "start_time",
            "end_time",
            "description"
        ]


class AddNewStudent(forms.ModelForm):
    class Meta:
        model = AssignedStudents
        fields =  "__all__"


class NewVirtualNetworkForm(forms.ModelForm):
    class Meta:
        model = VirtualNetwork
        fields = "__all__"


class CourseApprovalForm(forms.ModelForm):
    class Meta:
        model = VirtualNetwork
        # fields = "__all__"
        fields = [
            "ip_address",
            "topology_image",
            "ssh_file",
            "instructions"
        ]


class CourseChallengeForm(forms.ModelForm):
    class Meta:
        model = CourseChallenge
        fields = "__all__"