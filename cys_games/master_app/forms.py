from django import forms

from django.contrib.auth import get_user_model
User  = get_user_model()

from .models import Course, AssignedStudents, VirtualNetwork, CourseChallenge
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,)


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




class registerForm(forms.ModelForm):
    # username = forms.CharField(label='Username', widget = forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
    ), strip=False, help_text=password_validation.password_validators_help_text_html(),)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(
    ), strip=False, help_text="Both Passwords should be same.",)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
        ]

    def clean_password2(self):
        cd = self.cleaned_data
        if self.cleaned_data.get('password') != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']


    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)
