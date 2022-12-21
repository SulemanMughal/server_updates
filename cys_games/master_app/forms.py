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

    def __init__(self, *args, **kwargs):
        super(AddNewStudent, self).__init__(*args, **kwargs)
        self.fields['student'].queryset = User.objects.filter(is_student = True)


class NewVirtualNetworkForm(forms.ModelForm):
    class Meta:
        model = VirtualNetwork
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(NewVirtualNetworkForm, self).__init__(*args, **kwargs)
        excludes = [network.course.id for network in VirtualNetwork.objects.all()]
        # self.fields['course'].queryset = Course.objects.filter(is_student = True)
        self.fields['course'].queryset = Course.objects.all().exclude(id__in=excludes)



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