import json
import traceback
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib import messages

# ? forms
from .forms import (
    loginForm,
    CreateCourseForm, 
    AddNewStudent, 
    NewVirtualNetworkForm, 
    CourseChallengeForm, 
    CourseApprovalForm, 
    registerForm
)


# ? Models
from .models import Course, AssignedStudents, CourseChallenge, VirtualNetwork, ChallengeSubmission

# ? Decorators
from .decorators import (
    student_required,
    teacher_required,
    admin_required
)

# import user
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


# ? Home View
def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(reverse("admin:index"))
    template_name = "master_app/index.html"
    context = {
    }
    return render(request, template_name, context)


# TODO  :   User Login View
def UserLoginView(request):
    template_name = "master_app/login.html"
    if request.user.is_authenticated:
        return redirect("master_index")
    form = loginForm()
    context = {
        "form": form,

    }
    return render(request, template_name, context)


# TODO  :   User Login View Ajax
def UserLoginAjaxView(request):
    if request.method == "POST":
        form = loginForm(request.POST)
        valuenext = request.POST.get('next')
        if form.is_valid():
            try:
                u = authenticate(
                    request,
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password"]
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
                                "next_url": reverse("instructor-dasboard-url"),
                                "message": "Successfully Login as Instructor"
                            }))
                            return JsonResponse(content, status=200)

                        # TODO  :   Check for Student
                        elif u.is_student:
                            content = json.loads(json.dumps({
                                "next_url": reverse("student-dasboard-url"),
                                "message": "Successfully Login as Student"
                            }))
                            return JsonResponse(content, status=200)

                        # TODO  :   Check for Admin
                        elif u.is_admin:
                            content = json.loads(json.dumps({
                                "next_url": reverse("admin-dasboard-url"),
                                "message": "Successfully Login as Admin"
                            }))
                            return JsonResponse(content, status=200)

                        else:
                            content = json.loads(json.dumps({
                                "next_url": reverse("master_index"),
                                "message": "Successfully Login"
                            }))
                            return JsonResponse(content, status=200)
                    else:
                        content = json.loads(json.dumps({
                            "error": "User does not verify himself or he has been blocked from using our services due to violation of our terms and conditions."
                        }))
                        return JsonResponse(content, status=400)
                else:
                    content = json.loads(json.dumps({
                        "error": "Username or password has been entered incorrectly."
                    }))
                    return JsonResponse(content, status=400)
            except:
                traceback.print_exc()
                content = json.loads(json.dumps({
                    "error": "Please login after sometimes. Requests are not processed at this time."
                }))
                return JsonResponse(content, status=400)
        else:
            content = json.loads(json.dumps({
                "error": "Please entered correct information for respective required fields."
            }))
            return JsonResponse(content, status=400)
    else:
        content = json.loads(json.dumps({
            # "error" : settings.POST_METHOD_REQUIRED
            "error": "Requuired Request Method : Post"
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


# TODO  :   Admin Courses List
@login_required
@admin_required
def AdminCourseList(request):
    template_name = 'master_app/admin/courses_list.html'
    courses = Course.objects.all()
    context = {
        "courses": courses
    }
    return render(request, template_name, context)


@login_required
@admin_required
def AdminCreateCourse(request):
    template_name = 'master_app/admin/create_course.html'
    if request.method == "POST":
        # print(request.POST)
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.instructor = request.user
            new_course.save()
            # messages.success(request, "New course has been created")
            return redirect(reverse("admin-course-list-url"))
    else:
        form = CreateCourseForm()
    context = {
        "form": form
    }
    return render(request, template_name, context)


# TODO  :   Admin Course Details
@login_required
@admin_required
def AdminCourseDetails(request, course_id):
    template_name = 'master_app/admin/course_details.html'
    try:
        course = Course.objects.get(id=course_id)
        easy_challenges = course.coursechallenge_set.filter(levels=1)
        medium_challenges = course.coursechallenge_set.filter(levels=2)
        hard_challenges = course.coursechallenge_set.filter(levels=3)
        students = course.assignedstudents_set.all()
    except Course.DoesNotExist:
        messages.error(request, "Requested course does not exist.")
        return redirect(reverse("admin-course-list-url"))
    except:
        messages.error(request, "Requested page does not exist.")
        return redirect(reverse("admin-dasboard-url"))

    context = {
        "course": course,
        "easy_challenges": easy_challenges,
        "medium_challenges": medium_challenges,
        "hard_challenges": hard_challenges,
        "students": students,
    }
    return render(request, template_name, context)

# TODO  :   Admin Course Approval


@login_required
@admin_required
def AdminCourseApproval(request, vn_id):
    updated_obj = VirtualNetwork.objects.get(id=vn_id)
    if request.method == "POST":
        form = CourseApprovalForm(
            request.POST, request.FILES, instance=updated_obj)
        if form.is_valid():
            updated_obj = form.save()
            updated_obj.course.is_approved = "3"
            updated_obj.course.save()
            # updated_obj.save()
            messages.success(request, "Request has been approved.")
            return redirect(reverse("admin-courses-details-url", args=[updated_obj.course.id]))
    else:
        form = CourseApprovalForm()
    messages.success(request, "Request can't be proceed at this time.")
    return redirect(reverse("admin-courses-details-url", args=[updated_obj.course.id]))

    # template_name = ''
    # context = {
    #     "form" : form
    # }
    # return render(request, template_name, context)


# TODO  :   Admin Course Reject
@login_required
@admin_required
def AdminCourseReject(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        course.is_approved = "4"
        course.save()
        messages.success(request, "Course has been rejected")
        return redirect(reverse("admin-courses-details-url", args=[course_id]))
    except Course.DoesNotExist:
        messages.error(request, "Requested course does not exist.")
        return redirect(reverse("admin-course-list-url"))
    except:
        messages.error(request, "Requested page does not exist.")
        return redirect(reverse("admin-course-list-url"))


# TODO  :   Admin Virtual Network List
@login_required
@admin_required
def AdminVirtualNetworkList(request):
    template_name = 'master_app/admin/virutal_netwroks.html'
    context = {
        "networks": VirtualNetwork.objects.all()
    }
    return render(request, template_name, context)


# TODO  :   Admin Virtual Network Create
@login_required
@admin_required
def AdminVirtualNetworkCreate(request):
    template_name = 'master_app/admin/virutal_netwroks_new.html'
    if request.method == "POST":
        form = NewVirtualNetworkForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New Virtual Network has been added")
            if request.POST.get("next", None):
                return redirect(request.POST.get("next", None))
            return redirect(reverse("admin-virtual-network-url"))
    else:
        form = NewVirtualNetworkForm()
    context = {
        "form": form
    }
    return render(request, template_name, context)


# TODO  :   Admin Virtual Network Details
@login_required
@admin_required
def AdminVirtualNetworkDetails(request, vn_id):
    template_name = 'master_app/admin/virutal_netwroks_detail.html'
    try:
        virtual_network = VirtualNetwork.objects.get(id=vn_id)

    except VirtualNetwork.DoesNotExist:
        messages.error(request, "Requested Virtual Network does not exist.")
        return redirect(reverse("student-machines-url"))
    except:
        messages.error(request, "Requested page does not exist.")
        return redirect(reverse("student-dasboard-url"))
    context = {
        "virtual_network": virtual_network
    }
    return render(request, template_name, context)


# TODO : Admin Student List
@login_required
@admin_required
def AdminStudentList(request):
    template_name = 'master_app/admin/student_list.html'
    all_students = User.objects.filter(is_student=True)
    context = {
        "all_students": all_students
    }
    return render(request, template_name, context)


# TODO  :   Admin Create New Student
@login_required
@admin_required
def AdminStudentCreate(request):
    template_name="master_app/admin/student_create.html"
    if request.method!='POST':
            form = registerForm()
    else:
        form = registerForm(request.POST)
        if form.is_valid() :
            user = form.save(commit=False)
            user.active = True
            user.is_student = True
            user.set_password(form.cleaned_data['password2'])
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.save()
            messages.success(request, "New Student has been created")
            return redirect(reverse("admin-student-list-url"))
            # current_site = get_current_site(request)
            # message = render_to_string('user_management/acc_active_email.html', {
            #     'user':user, 
            #     'domain':current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            # mail_subject = 'Activate your account.'
            # to_email = form.cleaned_data.get('email')
            # email = EmailMessage(mail_subject, message, to=[to_email])
            # email.send()
            # return render(request, 'user_management/acc_active_email_confirm.html')
    context={
        'form' : form
    }
    return render(request, template_name, context)

# TODO  :   Admin Create New Instructor
@login_required
@admin_required
def AdminInstructorCreate(request):
    template_name="master_app/admin/instructor_create.html"
    if request.method!='POST':
            form = registerForm()
    else:
        form = registerForm(request.POST)
        if form.is_valid() :
            user = form.save(commit=False)
            user.active = True
            user.is_instructor = True
            user.set_password(form.cleaned_data['password2'])
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.save()
            messages.success(request, "New Instructor has been created")
            return redirect(reverse("admin-instructors-list-url"))
            # current_site = get_current_site(request)
            # message = render_to_string('user_management/acc_active_email.html', {
            #     'user':user, 
            #     'domain':current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            # mail_subject = 'Activate your account.'
            # to_email = form.cleaned_data.get('email')
            # email = EmailMessage(mail_subject, message, to=[to_email])
            # email.send()
            # return render(request, 'user_management/acc_active_email_confirm.html')
    context={
        'form' : form
    }
    return render(request, template_name, context)
    # return redirect(reverse("admin-dasboard-url"))
        

# TODO  :   Admin Instructors List
@login_required
@admin_required
def AdminInstructorsList(request):
    template_name = 'master_app/admin/instructor_list.html'
    all_teachers = User.objects.filter(is_instructor=True)
    context = {
        "all_teachers": all_teachers
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
    all_courses = Course.objects.filter(instructor=request.user)

    # print(all_courses)
    context = {
        "all_courses": all_courses
    }
    return render(request, template_name, context)


@login_required
@teacher_required
def StudentList(request):
    template_name = 'master_app/instructor/student_list.html'
    # TODO  :   Retrieve All Instructor Courses
    all_courses = Course.objects.filter(instructor=request.user)

    # TODO  :   Retrieve All Students
    all_students = []
    for i in all_courses:
        all_students.append(i.assignedstudents_set.all())
    context = {
        "all_students": all_students
    }
    return render(request, template_name, context)


# TODO  :   Instructor Create New Course
@login_required
@teacher_required
def CreateCourse(request):
    template_name = 'master_app/instructor/create_course.html'
    if request.method == "POST":
        # print(request.POST)
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.instructor = request.user
            new_course.save()
            # messages.success(request, "New course has been created")
            return redirect(reverse("courses-all-url"))
    else:
        form = CreateCourseForm()
    context = {
        "form": form
    }
    return render(request, template_name, context)


# TODO  :   Instructor Create New Challenge
@login_required
@teacher_required
def InstructorCreateNewChallenge(request):
    template_name = 'master_app/instructor/create_new_challenge.html'
    if request.method == "POST":
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
        "form": form
    }
    return render(request, template_name, context)

# TODO  :   Instructor Course Details


@login_required
@teacher_required
def InstructorCourseDetails(request, course_id):
    template_name = 'master_app/instructor/courseDetails.html'
    try:
        course = Course.objects.get(id=course_id)
        easy_challenges = course.coursechallenge_set.filter(levels=1)
        medium_challenges = course.coursechallenge_set.filter(levels=2)
        hard_challenges = course.coursechallenge_set.filter(levels=3)
        students = course.assignedstudents_set.all()
    except Course.DoesNotExist:
        messages.error(request, "Invalid Course URL")
        return redirect(reverse("courses-all-url"))
    except Exception as e:
        messages.error(
            request, "Plase try again after some time or contact admin.")
        return redirect(reverse("master_index"))

    context = {
        "course": course,
        "easy_challenges": easy_challenges,
        "medium_challenges": medium_challenges,
        "hard_challenges": hard_challenges,
        "students": students,
        "form":  NewVirtualNetworkForm(),
        "form_2":  AddNewStudent(),
    }
    return render(request, template_name, context)


# TODO  :   Instructor Course Challenge Details
@login_required
@teacher_required
def InstructorChallengeDetails(request, course_id, challenge_id):
    template_name = 'master_app/instructor/challenge_details.html'
    try:
        course = Course.objects.get(id=course_id)
        challenge = CourseChallenge.objects.get(id=challenge_id)
    except (Course.DoesNotExist, CourseChallenge.DoesNotExist):
        messages.error(request, "Invalid URL")
        return redirect(reverse("courses-all-url"))
    except Exception as e:
        messages.error(
            request, "Plase try again after some time or contact admin.")
        return redirect(reverse("master_index"))
    context = {
        "course": course,
        "challenge": challenge
    }
    return render(request, template_name, context)


# ! Depreciated
# TODO  :   Instructor
@login_required
@teacher_required
def InstructorApproveCourse(request, course_id):

    try:
        course = Course.objects.get(id=course_id)
        course.is_approved = "2"
        course.save()
        messages.success(
            request, "Approval Request to admin has been sent successfully.")
        return redirect(reverse("instructor-courses-details-url", args=[course_id]))
    # except Course.DoesNotExist:
    #     messages.error(request, "Requested URL Does not Exist")
    #     return redirect(reverse("courses-all-url"))
    except:
        messages.error(request, "Requested URL Does not Exist")
        return redirect(reverse("courses-all-url"))

    # if request.method == "POST" :
    #     return JsonResponse(
    #         json.loads(
    #             json.dumps({
    #                 "text" : "Valid method"
    #             })
    #         ),
    #         status =200
    #     )

    # else:
    #     return JsonResponse(
    #         json.loads(
    #             json.dumps({
    #                 "error" : "Invalid request method"
    #             })
    #         ),
    #         status =400
    #     )


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
            if request.POST.get("next", None):
                return redirect(request.POST.get("next", None))
            return redirect(reverse("instructor-virtual-network-url"))
    else:
        form = NewVirtualNetworkForm()
    context = {
        "form": form
    }
    return render(request, template_name, context)

# TODO  :   Instructor Virutal Networks List


@login_required
@teacher_required
def InstructorVirtualNetworkList(request):
    networks = [i for x in Course.objects.filter(
        instructor=request.user) for i in x.virtualnetwork_set.all() if len(x.virtualnetwork_set.all()) > 0]
    template_name = 'master_app/instructor/virutal_netwroks.html'
    context = {
        "networks": networks
    }
    return render(request, template_name, context)


# TODO  :   Instructor Virutal Networks Details
@login_required
@teacher_required
def InstructorMachineDetail(request, vn_id):
    template_name = 'master_app/instructor/network_detail.html'
    try:
        virtual_network = VirtualNetwork.objects.get(id=vn_id)

    except VirtualNetwork.DoesNotExist:
        messages.error(request, "Requested Virtual Network does not exist.")
        return redirect(reverse("student-machines-url"))
    except:
        messages.error(request, "Requested page does not exist.")
        return redirect(reverse("student-dasboard-url"))
    context = {
        "virtual_network": virtual_network
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
        "form": form
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
    courses = AssignedStudents.objects.filter(
        student__id=request.user.id).filter(course__is_approved="3")
    # print(courses)

    context = {
        "courses": courses
    }
    return render(request, template_name, context)


# TODO  :   Student Course Details
@login_required
@student_required
def StudentCourseDetails(request, course_id):
    template_name = 'master_app/student/courseDetails.html'
    try:
        course = Course.objects.get(id=course_id, is_approved="3")
        easy_challenges = course.coursechallenge_set.filter(levels=1)
        medium_challenges = course.coursechallenge_set.filter(levels=2)
        hard_challenges = course.coursechallenge_set.filter(levels=3)
    except:
        messages.error(request, "Requested course does not exist")
        return redirect(reverse("student-courses-url"))

    context = {
        "course": course,
        "easy_challenges": easy_challenges,
        "medium_challenges": medium_challenges,
        "hard_challenges": hard_challenges
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
    # TODO  :   Retrieve All courses
    courses = AssignedStudents.objects.filter(
        student__id=request.user.id).filter(course__is_approved="3")
    # print(courses)
    networks = [i for x in courses for i in x.course.virtualnetwork_set.all(
    ) if len(x.course.virtualnetwork_set.all()) > 0]

    # print(networks)
    context = {
        "networks": networks
    }
    return render(request, template_name, context)


# TODO  :   Students Network Detail
@login_required
@student_required
def StudentMachineDetail(request, vn_id):
    template_name = 'master_app/student/machine_detail.html'
    try:
        virtual_network = VirtualNetwork.objects.get(id=vn_id)

    except VirtualNetwork.DoesNotExist:
        messages.error(request, "Requested Virtual Network does not exist.")
        return redirect(reverse("student-machines-url"))
    except:
        messages.error(request, "Requested page does not exist.")
        return redirect(reverse("student-dasboard-url"))
    context = {
        "virtual_network": virtual_network
    }
    return render(request, template_name, context)


# TODO  :   Student Challenge Details
@login_required
@student_required
def StudentChallengeDetails(request, course_id, challenge_id):
    template_name = 'master_app/student/challenge_details.html'
    try:
        course = Course.objects.get(id=course_id)
        if course.course_status() == 1:
            messages.error(
                request, "Challenges can't be accessed before course")
            return redirect(reverse("student-courses-details-url", args=[course_id]))
        challenge = CourseChallenge.objects.get(id=challenge_id)
        assigned_student = AssignedStudents.objects.get(
            course=course,
            student=request.user
        )
        if challenge.levels == "3":
            if not assigned_student.is_all_easy_challenges_submitted():
                messages.error(
                    request, "Please submit all EASY level challenges first.")
                return redirect(reverse("student-courses-details-url", args=[course_id]))
            elif not assigned_student.is_all_medium_challenges_submitted():
                messages.error(
                    request, "Please submit all MEDIUM level challenges first.")
                return redirect(reverse("student-courses-details-url", args=[course_id]))
        elif challenge.levels == "2":
            if not assigned_student.is_all_easy_challenges_submitted():
                messages.error(
                    request, "Please submit all EASY level challenges first.")
                return redirect(reverse("student-courses-details-url", args=[course_id]))

        try:
            submission_obj = ChallengeSubmission.objects.get(
                assinged_student=assigned_student,
                challenge=challenge
            )
        except ChallengeSubmission.DoesNotExist:
            submission_obj = ChallengeSubmission.objects.create(
                assinged_student=assigned_student,
                challenge=challenge,
                status="PENDING"
            )
        # try:
        #     # TODO  :   Get TaskSubmission instance
        #     submission_obj = ChallengeSubmission.objects.get(
        #         assinged_student = course,
        #         challenge_id = obj.task_id,
        #         content_type = ContentType.objects.get_for_model(
        #             obj
        #         )
        #     )
        # except TaskSubmission.DoesNotExist:
        #     task_submission_obj = TaskSubmission.objects.create(
        #         assinged_event = ctf_obj,
        #         challenge_id = obj.task_id,
        #         content_object = obj
        #     )
        # except Exception as e:
        #     logger.error(e, exc_info=sys.exc_info())
        #     messages.error(request, settings.GENERAL_EXCEPTION_ERROR)
        #     return redirect(reverse("master-home"))
    except (Course.DoesNotExist, CourseChallenge.DoesNotExist, AssignedStudents.DoesNotExist):
        messages.error(request, "Invalid URL")
        return redirect(reverse("student-courses-url"))
    except Exception as e:
        messages.error(
            request, "Plase try again after some time or contact admin.")
        return redirect(reverse("master_index"))
    context = {
        "course": course,
        "challenge": challenge,
        "submission_obj": submission_obj
    }
    return render(request, template_name, context)


# TODO  :   Student Challenge Flag Submission
@login_required
@student_required
def StudentChallengeFlagSubmission(request, course_id, challenge_id, submission_id):
    try:
        if request.method == "POST":
            # print(request.POST)
            course = Course.objects.get(id=course_id)
            challenge = CourseChallenge.objects.get(
                course__id=course.id, id=challenge_id)
            assigned_student = AssignedStudents.objects.get(
                course=course,
                student=request.user
            )
            submission_obj = ChallengeSubmission.objects.get(
                assinged_student=assigned_student,
                challenge=challenge,
                id=submission_id
            )

            if request.POST.get("flag", None):
                if request.POST.get("flag", None) == challenge.original_flag:
                    submission_obj.submitted_answer = request.POST['flag']
                    submission_obj.status = "SUBMITTED"
                    submission_obj.obtained_points = (
                        challenge.points) - (submission_obj.attempts*5)
                    submission_obj.attempts = (submission_obj.attempts) + 1
                    submission_obj.save()
                    messages.success(request, "Correct Flag")
                    return redirect(reverse("student-challenge-details-url", args=[course_id, challenge_id]))
            submission_obj.attempts = int(submission_obj.attempts)+1
            submission_obj.save()
            messages.error(request, "Wrong Flag Submission")
            return redirect(reverse("student-challenge-details-url", args=[course_id, challenge_id]))
        else:
            messages.error(request, "Requested page does not exist")
            return redirect(reverse("student-dasboard-url"))
    except:
        messages.error(request, "Requested page does not exist")
        return redirect(reverse("student-dasboard-url"))

    # template_name = ''
    # context = {
    # }
    # return render(request, template_name, context)


# TODO  :   Student Create Virtual Network Instance

def StudentCreateNetworkInstance(request):
    if request.method == "POST":
        return JsonResponse(
            json.loads(
                json.dumps({
                    "message": "Valid method"
                })
            ),
            status=200
        )

    else:
        return JsonResponse(
            json.loads(
                json.dumps({
                    "error": "Invalid request method"
                })
            ),
            status=400
        )
