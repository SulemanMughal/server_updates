import json, traceback
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib import messages

# ? forms
from .forms import loginForm, CreateCourseForm, AddNewStudent, NewVirtualNetworkForm, CourseChallengeForm


# ? Models
from .models import Course, AssignedStudents, CourseChallenge

# ? Decorators
from .decorators import (
    student_required, 
    teacher_required,
    admin_required
)
# Create your views here.




# ? Home View
def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(reverse("admin:index"))
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


# TODO  :   Admin Profile
@login_required
@admin_required
def AdminProfile(request):
    template_name = 'master_app/admin/profile.html'
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


# TODO  :   Instructor Profile
@login_required
@teacher_required
def InsturctorProfile(request):
    template_name = 'master_app/instructor/profile.html'
    context = {
    }
    return render(request, template_name, context)

@login_required
@teacher_required
def CoursesList(request):
    template_name = 'master_app/instructor/courses_list.html'

    # TODO : Retrieve All Instructor Courses
    all_courses = Course.objects.filter(instructor = request.user)

    # print(all_courses)
    context = {
        "all_courses" : all_courses
    }
    return render(request, template_name, context)

@login_required
@teacher_required
def StudentList(request):
    template_name = 'master_app/instructor/student_list.html'
    # TODO  :   Retrieve All Instructor Courses
    all_courses = Course.objects.filter(instructor = request.user)

    # TODO  :   Retrieve All Students
    all_students = []
    for i in all_courses:
        all_students.append(i.assignedstudents_set.all())
    context = {
        "all_students" : all_students
    }
    return render(request, template_name, context)



# TODO  :   Instructor Create New Course
@login_required
@teacher_required
def CreateCourse(request):
    template_name = 'master_app/instructor/create_course.html'
    if request.method == "POST" : 
        # print(request.POST)
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            new_course = form.save(commit = False)
            new_course.instructor = request.user
            new_course.save()
            # messages.success(request, "New course has been created")
            return redirect(reverse("courses-all-url"))
    else:
        form = CreateCourseForm()
    context = {
        "form" : form
    }
    return render(request, template_name, context)



# TODO  :   Instructor Create New Challenge
@login_required
@teacher_required
def InstructorCreateNewChallenge(request):
    template_name = 'master_app/instructor/create_new_challenge.html'
    if request.method  == "POST":
        form = CourseChallengeForm(request.POST)
        # print(request.POST["next"])
        # print(request.POST)
        form.save()
        messages.success(request, "New Challenge has been added.")
        if request.POST.get("next", None):
            return redirect(request.POST.get("next", None))
        return redirect("courses-all-url")

    form = CourseChallengeForm()
    context = {
        "form" : form
    }
    return render(request, template_name, context)

# TODO  :   Instructor Course Details
@login_required
@teacher_required
def InstructorCourseDetails(request, course_id):
    template_name = 'master_app/instructor/courseDetails.html'
    try:
        course = Course.objects.get(id = course_id)
        easy_challenges = course.coursechallenge_set.filter(levels = 1)
        medium_challenges = course.coursechallenge_set.filter(levels = 2)
        hard_challenges = course.coursechallenge_set.filter(levels = 3)
        students = course.assignedstudents_set.all()
    except Course.DoesNotExist:
        messages.error(request, "Invalid Course URL")
        return redirect(reverse("courses-all-url"))
    except Exception as e:
        messages.error(request, "Plase try again after some time or contact admin.")
        return redirect(reverse("master_index"))
    
    context = {
        "course"  : course,
        "easy_challenges" : easy_challenges,
        "medium_challenges" : medium_challenges,
        "hard_challenges" : hard_challenges,
        "students" : students,
        "form" :  NewVirtualNetworkForm(),
        "form_2" :  AddNewStudent(),
    }
    return render(request, template_name, context)


# TODO  :   Instructor Course Challenge Details
@login_required
@teacher_required
def InstructorChallengeDetails(request, course_id, challenge_id):
    template_name = 'master_app/instructor/challenge_details.html'
    try:
        course = Course.objects.get(id = course_id)
        challenge = CourseChallenge.objects.get(id = challenge_id)
    except (Course.DoesNotExist, CourseChallenge.DoesNotExist):
        messages.error(request, "Invalid URL")
        return redirect(reverse("courses-all-url"))
    except Exception as e:
        messages.error(request, "Plase try again after some time or contact admin.")
        return redirect(reverse("master_index"))
    context = {
        "course" : course,
        "challenge" : challenge
    }
    return render(request, template_name, context)



# TODO  :   Instructor Virutal Networks Create New
@login_required
@teacher_required
def InstructorVirturalNetworkNew(request):
    template_name = 'master_app/instructor/virutal_netwroks_new.html'
    if request.method == "POST":
        form = NewVirtualNetworkForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New Network Machine Has been added")
            if request.POST.get("next" , None):
                return redirect(request.POST.get("next" , None))
            return redirect(reverse("instructor-virtual-network-url"))
    else:
        form = NewVirtualNetworkForm()
    context = {
        "form" : form
    }
    return render(request, template_name, context)

# TODO  :   Instructor Virutal Networks List
@login_required
@teacher_required
def InstructorVirtualNetworkList(request):
    networks = [i for x in Course.objects.filter(instructor = request.user) for i in x.virtualnetwork_set.all() if len(x.virtualnetwork_set.all())>0 ]
    template_name = 'master_app/instructor/virutal_netwroks.html'
    context = {
        "networks" : networks
    }
    return render(request, template_name, context)





# TODO  :   Add New Students To A Course
@login_required
@teacher_required
def AddNewStudents(request):
    template_name = 'master_app/instructor/add_new_student.html'
    if request.method == "POST":
        form = AddNewStudent(request.POST)
        # print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New Student has been added")
            if request.POST.get("next", None):
                return redirect(request.POST.get("next", None))
            return redirect(reverse("students-all-url"))
        # else:
        #     print(form.errors)
        #     messages.error(request, str())

    else:
        form = AddNewStudent()
    context = {
        "form" : form
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


# TODO  :   Student Courses
@login_required
@student_required
def StudentCourses(request):
    template_name = 'master_app/student/courseList.html'
    courses = AssignedStudents.objects.filter(student__id = request.user.id).filter(course__is_approved="Approved")
    # print(courses)
    
    context = {
        "courses" : courses
    }
    return render(request, template_name, context)


# TODO  :   Student Course Details
@login_required
@student_required
def StudentCourseDetails(request , course_id):
    template_name = 'master_app/student/courseDetails.html'
    try:
        course = Course.objects.get(id=course_id, is_approved = "Approved")
        easy_challenges = course.coursechallenge_set.filter(levels = 1)
        medium_challenges = course.coursechallenge_set.filter(levels = 2)
        hard_challenges = course.coursechallenge_set.filter(levels = 3)
    except:
        messages.error(request, "Requested course does not exist")
        return redirect(reverse("student-courses-url"))
    
    context = {
        "course" : course,
        "easy_challenges" : easy_challenges,
        "medium_challenges" : medium_challenges,
        "hard_challenges" : hard_challenges
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



# TODO  :   Students Machines List
@login_required
@student_required
def StudentMachines(request):
    template_name = 'master_app/student/machines.html'
    context = {
    }
    return render(request, template_name, context)



# TODO  :   Students Machine Detail
@login_required
@student_required
def StudentMachineDetail(request):
    template_name = 'master_app/student/machine_detail.html'
    context = {
    }
    return render(request, template_name, context)


# TODO  :   Student Challenge Details
@login_required
@student_required
def StudentChallengeDetails(request, course_id, challenge_id):
    template_name = 'master_app/student/challenge_details.html'
    try:
        course = Course.objects.get(id = course_id)
        challenge = CourseChallenge.objects.get(id = challenge_id)
    except (Course.DoesNotExist, CourseChallenge.DoesNotExist):
        messages.error(request, "Invalid URL")
        return redirect(reverse("courses-all-url"))
    except Exception as e:
        messages.error(request, "Plase try again after some time or contact admin.")
        return redirect(reverse("master_index"))
    context = {
        "course" : course,
        "challenge" : challenge
    }
    return render(request, template_name, context)