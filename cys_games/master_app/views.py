import json, traceback
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator

# ? forms
from .forms import loginForm

# ? Decorators
from .decorators import (
    student_required, 
    teacher_required,
    admin_required
)
# Create your views here.




# ? Home View
def index(request):
    template_name= "master_app/index.html"
    context = {
    }
    return render(request, template_name, context)


# TODO  :   User Login View
def UserLoginView(request):
    template_name= "master_app/login.html"
    if request.user.is_authenticated:
        return redirect("master_index")
    form = loginForm()
    context = {
        "form" : form,
        
    }
    return render(request, template_name, context)



# TODO  :   User Login View Ajax
def UserLoginAjaxView(request):
    if request.method == "POST" :
        form = loginForm(request.POST)
        valuenext = request.POST.get('next')
        if form.is_valid():
            try:
                u = authenticate(
                    request, 
                    email = form.cleaned_data["email"], 
                    password = form.cleaned_data["password"]
                )
                if u is not None:
                    if u.is_active:
                        login(request, u)
                        # if len(valuenext) != 0 and valuenext is not None:
                        #     content = json.loads(json.dumps({
                        #         "next_url" : valuenext,
                        #         "message" : "Successfully Login as Instructor"
                        #     }))
                        #     return JsonResponse(content, status=200)
                        # else:
                        #     content = json.loads(json.dumps({
                        #         "next_url" : reverse("master_index"),
                        #         "message" : "Successfully Login as Instructor"
                        #     }))
                        #     return JsonResponse(content, status=200)

                        # TODO  :   Check if login-user is an instructor
                        if u.is_instructor:
                            content = json.loads(json.dumps({
                                "next_url" : reverse("instructor-dasboard-url"),
                                "message" : "Successfully Login as Instructor"
                            }))
                            return JsonResponse(content, status=200)
                        
                        # TODO  :   Check for Student
                        elif u.is_student:
                            content = json.loads(json.dumps({
                                "next_url" : reverse("student-dasboard-url"),
                                "message" : "Successfully Login as Student"
                            }))
                            return JsonResponse(content, status=200)
                        
                        # TODO  :   Check for Admin
                        elif u.is_admin:
                            content = json.loads(json.dumps({
                                "next_url" : reverse("admin-dasboard-url"),
                                "message" : "Successfully Login as Admin"
                            }))
                            return JsonResponse(content, status=200)


                        else:
                            content = json.loads(json.dumps({
                                "next_url" : reverse("master_index"),
                                "message" : "Successfully Login"
                            }))
                            return JsonResponse(content, status=200)
                    else:
                        content = json.loads(json.dumps({
                            "error" : "User does not verify himself or he has been blocked from using our services due to violation of our terms and conditions."
                        }))
                        return JsonResponse(content, status=400)
                else:
                    content = json.loads(json.dumps({
                        "error" : "Username or password has been entered incorrectly."
                    }))
                    return JsonResponse(content, status=400)
            except:
                traceback.print_exc()
                content = json.loads(json.dumps({
                        "error" : "Please login after sometimes. Requests are not processed at this time."
                    }))
                return JsonResponse(content, status=400)
        else:
            content = json.loads(json.dumps({
                "error" : "Please entered correct information for respective required fields."
            }))
            return JsonResponse(content, status=400)
    else:
        content = json.loads(json.dumps({
            # "error" : settings.POST_METHOD_REQUIRED
            "error" : "Requuired Request Method : Post"
        }))
        return JsonResponse(content, status=400)



# TODO  :   User Logout View
def UserLogoutView(request):
    logout(request)
    return redirect('master_index')


# TODO  :   Admin Dashboard
@login_required
@admin_required
def AdminDashboard(request):
    template_name = 'master_app/admin/dashboard.html'
    context = {
    }
    return render(request, template_name, context)


# TODO  :   Instructor Dashboard
@login_required
@teacher_required
def InstructorDashboard(request):
    template_name = 'master_app/instructor/dashboard.html'
    context = {
    }
    return render(request, template_name, context)

# TODO  :   Student Dashboard
# @method_decorator([login_required, student_required], name='dispatch')
@login_required
@student_required
def StudentDashboard(request):
    template_name = 'master_app/student/dashboard.html'
    context = {
    }
    return render(request, template_name, context)

# TODO  :   Student Profile
@login_required
@student_required
def StudentProfile(request):
    template_name = 'master_app/student/profile.html'
    context = {
    }
    return render(request, template_name, context)