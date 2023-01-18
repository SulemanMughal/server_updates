import os
import uuid 
import json
import time
import requests
import traceback
import subprocess
from django.urls import reverse
from django.core.files import File
from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
# from django.contrib.admin.models import  LogEntry
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE

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
from .models import Course, AssignedStudents, CourseChallenge, VirtualNetwork, ChallengeSubmission,NetworkFlag, NetworkFlagSubmission

# ? Decorators
from .decorators import (
    student_required,
    teacher_required,
    admin_required
)

# import settigns
from django.conf import settings

# import user
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


# ? Development Print Functions
def customPrint(message):
    if settings.DEBUG:
        print("="*70)
        print(message)
        print("="*70)

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
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str


def get_content_type_for_model(obj):
    return ContentType.objects.get_for_model(obj, for_concrete_model=False)

def get_field_value(obj, field):
        return getattr(obj, field)

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
                        try:
                            LogEntry.objects.create(
                                user = u,
                                action_flag=ADDITION,
                                object_id=u.id,
                                content_type_id=get_content_type_for_model(u).pk,
                                object_repr=force_str(u),
                                change_message = f"{u} has been loggin."
                            )
                        except Exception as e:
                            print(e)
                        # LogEntry.objects.log_action(
                        #     user_id=u,
                        #     content_type_id=get_content_type_for_model(object).pk,
                        #     object_id=object.pk,
                        #     object_repr=force_text(object),
                        #     action_flag=ADDITION
                        # ) 

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
            "error": "Requuired Request Method : Post"
        }))
        return JsonResponse(content, status=400)


# TODO  :   User Logout View
def UserLogoutView(request):
    logout(request)
    return redirect('master_index')


# TODO  :   How to Connect VPN
def ConnectVPN(request):
    template_name="master_app/connect_vpn.html"
    context = {

    }
    return render(request, template_name, context)


# TODO  :   Admin Dashboard
@login_required
@admin_required
def AdminDashboard(request):
    template_name = 'master_app/admin/dashboard.html'
    
    # TODO  :   Retrieve All Instructors
    instructors = User.objects.filter(is_instructor = True)
    
    # TODO  :   Retrieve All Instructors
    students = User.objects.filter(is_student = True)

    # TODO  :   Retrieve All Courses
    courses = Course.objects.all().order_by("-created_timestamp")

    # TODO  :   Retrieve All Local Virutal Networks
    networks = VirtualNetwork.objects.all()

    # TODO  :   Recent Acitivty 
    entries = LogEntry.objects.exclude(
        user__username = "developer"
    )
    
    context = {
        "instructors"  : instructors,
        "students" : students,
        "courses" : courses,
        "networks" : networks,
        "entries" : entries
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
    courses = Course.objects.all().order_by("-id")
    context = {
        "courses": courses
    }
    return render(request, template_name, context)


@login_required
@admin_required
def AdminCreateCourse(request):
    template_name = 'master_app/admin/create_course.html'
    if request.method == "POST":
        form = CreateCourseForm(request.POST, request.FILES)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.instructor = request.user
            new_course.save()
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
        "WAZUH_SERVER_PUBLIC_IP" : settings.WAZUH_SERVER_PUBLIC_IP,
        "DC_IP_ADDRESS" : settings.DC_IP_ADDRESS
    }
    return render(request, template_name, context)

# TODO  :   Admin Course Approval
@login_required
@admin_required
def AdminCourseApproval(request, vn_id):
    updated_obj = VirtualNetwork.objects.get(id=vn_id)
    if request.method == "GET":
        updated_obj.course.is_approved = "3"
        updated_obj.course.save()
        updated_obj.save()
        return JsonResponse(
            json.loads(
                json.dumps({
                    "text" : "Course has been approved."
                })
            ),
            status =200
        )
    else:
        return JsonResponse(
            json.loads(
                json.dumps({
                    "error" : "Invalid request method"
                })
            ),
            status =400
        )

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
            user.is_active = True
            user.is_student = True
            user.set_password(form.cleaned_data['password2'])
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.save()
            messages.success(request, "New Student has been created")
            return redirect(reverse("admin-student-list-url"))
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
            user.is_active = True
            user.is_instructor = True
            user.set_password(form.cleaned_data['password2'])
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.save()
            messages.success(request, "New Instructor has been created")
            return redirect(reverse("admin-instructors-list-url"))
    context={
        'form' : form
    }
    return render(request, template_name, context)


# TODO  :   Admin - Add a new challenge to an existing course
@login_required  
@admin_required
def AdminChallengeCreate(request):
    template_name = 'master_app/admin/create_new_challenge.html'
    if request.method == "POST":
        form = CourseChallengeForm(request.POST)
        form.save()
        messages.success(request, "New Challenge has been added.")
        if request.POST.get("next", None):
            return redirect(request.POST.get("next", None))
        return redirect("admin-course-list-url")

    form = CourseChallengeForm()
    context = {
        "form": form
    }
    return render(request, template_name, context)


# TODO  :   Admin   -   Add a new student to an existing course
@login_required
@admin_required
def AdminCourseStudentCreate(request):
    template_name = 'master_app/admin/add_new_student.html'
    if request.method == "POST":
        form = AddNewStudent(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New Student has been added")
            if request.POST.get("next", None):
                return redirect(request.POST.get("next", None))
            return redirect(reverse("students-all-url"))
    else:
        form = AddNewStudent()
    context = {
        "form": form
    }
    return render(request, template_name, context)


# TODO  :   Admin Fetch Network Images from OpenStack
def AdminFetchNetworkImages(request):
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
    'auth': {
        'identity': {
            'methods': [
                'password',
            ],
            'password': {
                'user': {
                    'name': settings.OPENSTACK_USER,
                    'domain': {
                        'id': 'default',
                    },
                    'password': settings.OPENSTACK_PASSWORD,
                },
            },
        },
        "scope": {
        "project": {
            "name": "admin",
            "domain": { 
                "id": "default" 
            }
        }
    }
        
    },
    }
    s = requests.Session()
    response = s.post(settings.OPENSTACK_AUTHORIZED_URL, headers=headers, json=json_data)
    if response.status_code in [200, 201, 202]:
        headers = {
            'X-Auth-Token': f'{response.headers["x-subject-token"]}',   
        }
        response = s.get(settings.OPENSTACK_IMAGE_URL, headers=headers )
        if response.status_code in [200, 201, 202]:
            return JsonResponse(
                json.loads(
                    json.dumps({
                        "data" : response.json()
                    })
                ),
                status =200
            )
        else:
            print("="*30, "OPENSTACK IMAGES URL", "-"*30, response.json(), "="*30, sep="\n")
            return JsonResponse(
            json.loads(
                json.dumps({
                    "error" : str(response.json()["error"]["message"]) 
                })
            ),
            status = 400
        )
    else:
        print("="*30, "OPENSTACK AUTHENTICATION ERROR", "-"*30, response.json(), "="*30, sep="\n")
        return JsonResponse(
            json.loads(
                json.dumps({
                    "error" : str( response.json()["error"]["message"] )
                })
            ),
            status =400
        )

# TODO  :  # ? Start an instance in openstack
def AdminStartNetworkInstance(request, vn_id):
    try:
        netObj = VirtualNetwork.objects.get(id = vn_id)
        headers = {
            'Content-Type': 'application/json',
        }
        json_data = {
            'auth': {
                'identity': {
                    'methods': [
                        'password',
                    ],
                    'password': {
                        'user': {
                            'name': settings.OPENSTACK_USER,
                            'domain': {
                                'id': 'default',
                            },
                            'password': settings.OPENSTACK_PASSWORD,
                        },
                    },
                },
                "scope": {
                "project": {
                "name": "admin",
                "domain": { "id": "default" }
                }
            }
                
            },
        }
        s = requests.Session()
        print("--> OPENSTACK SESSION STARTED")
        response = s.post(settings.OPENSTACK_AUTHORIZED_URL, headers=headers, json=json_data)
        print("--> OPENSTACK AUTHORIZATION STARTED")
        if response.status_code in [200, 201, 202]:
            headers = {
                'X-Auth-Token': f'{response.headers["x-subject-token"]}',   
            }
            print("--> OPENSTACK DETAILS DOMAIN CLIENT REQUEST STARTED")
            response = s.get(f"{settings.OPENSTACK_SERVER_URL}/{settings.DC_CLIENT_SERVER}", headers=headers )
            if response.status_code in [200, 201, 202]:                
                if(response.json()["server"]["status"] != "ACTIVE" ):
                    json_data={
                        "os-start" : None
                    }
                    print("--> OPENSTACK ACTIVE DOMAIN CLIENT REQUEST STARTED")
                    response = s.post(f"{settings.OPENSTACK_SERVER_URL}/{settings.DC_CLIENT_SERVER}/action", headers=headers , json=json_data)
                    if response.status_code in [200, 201, 202]:
                        print("--> OPENSTACK GET DOMAIN CLIENT PUBLIC IP REQUEST STARTED")
                        response = s.get(f"{settings.OPENSTACK_SERVER_URL}/{settings.DC_CLIENT_SERVER}/ips/{settings.OPENSTACK_NETWORK_LABEL}", headers=headers )
                        if response.status_code in [200, 201, 202]:
                            netObj.server_id = settings.DC_CLIENT_SERVER
                            netObj.ip_address = response.json()["demo-net"][1]["addr"]
                            netObj.is_instance_created = True
                            netObj.save()
                            print("--> OPENSTACK GET DOMAIN CLIENT FLAGS REQUEST STARTED")
                            response = s.get(f"{settings.OPENSTACK_SERVER_URL}/{settings.DC_CLIENT_SERVER}/metadata", headers=headers )
                            if response.status_code in [200, 201, 202]:
                                print("--> OPENSTACK SAVE DOMAIN CLIENT FLAGS TO LOCAL DB REQUEST STARTED")
                                for i in response.json()["metadata"]:
                                    if i[:4].lower() == "flag":
                                        try:
                                            netFlag = NetworkFlag.objects.get_or_create(
                                                course = netObj.course,
                                                flag_id = i
                                            )
                                            netFlag[0].original_answer = response.json()["metadata"][i]
                                            netFlag[0].points = 50
                                            netFlag[0].imageRef = netObj.imageRef
                                            netFlag[0].save()
                                        except Exception as e:
                                            print("--> EXCEPTION OCCURED")
                                            traceback.print_exc() 
                                print(NetworkFlag.objects.all())
                                return JsonResponse(
                                    json.loads(
                                        json.dumps({
                                            "data" : "Instance has been activated successfully"
                                        })
                                    ),
                                    status =200
                                )
                            else:
                                print("--> PENSTACK SAVE DOMAIN CLIENT FLAGS TO LOCAL DB REQUEST STARTED")
                                print(response.content)
                                return JsonResponse(
                                    json.loads(
                                        json.dumps({

                                            "error" : str( response.json()["error"]["message"] )
                                        })
                                    ),
                                    status =400
                                )
                        else:
                            print("--> OPENSTACK GET DOMAIN CLIENT PUBLIC IP REQUEST ERROR")
                            print(response.content)
                            return JsonResponse(
                                json.loads(
                                    json.dumps({

                                        "error" : str( response.json()["error"]["message"] )
                                    })
                                ),
                                status =400
                            )
                    else:
                        print("--> OPENSTACK ACTIVE DOMAIN CLIENT REQUEST ERROR")
                        print(response.content)
                        return JsonResponse(
                            json.loads(
                                json.dumps({

                                    "error" : str( response.json()["error"]["message"] )
                                })
                            ),
                            status =400
                        )
                else:
                    print("--> OPENSTACK RESUME DOMAIN CLIENT REQUEST STARTED")
                    print("--> OPENSTACK GET DOMAIN CLIENT PUBLIC IP REQUEST STARTED")
                    response = s.get(f"{settings.OPENSTACK_SERVER_URL}/{settings.DC_CLIENT_SERVER}/ips/{settings.OPENSTACK_NETWORK_LABEL}", headers=headers )
                    if response.status_code in [200, 201, 202]:
                        netObj.server_id = settings.DC_CLIENT_SERVER
                        netObj.ip_address = response.json()["demo-net"][1]["addr"]
                        netObj.is_instance_created = True
                        netObj.save()
                        print("--> OPENSTACK GET DOMAIN CLIENT FLAGS REQUEST STARTED")
                        response = s.get(f"{settings.OPENSTACK_SERVER_URL}/{settings.DC_CLIENT_SERVER}/metadata", headers=headers )
                        if response.status_code in [200, 201, 202]:
                            print("--> OPENSTACK SAVE DOMAIN CLIENT FLAGS TO LOCAL DB REQUEST STARTED")
                            for i in response.json()["metadata"]:
                                if i[:4].lower() == "flag":
                                    try:
                                        netFlag = NetworkFlag.objects.get_or_create(
                                            course = netObj.course,
                                            flag_id = i
                                        )
                                        netFlag[0].original_answer = response.json()["metadata"][i]
                                        netFlag[0].points = 50
                                        netFlag[0].imageRef = netObj.imageRef
                                        netFlag[0].save()
                                    except Exception as e:
                                        print("--> EXCEPTION OCCURED")
                                        traceback.print_exc() 
                            print(NetworkFlag.objects.all())
                            return JsonResponse(
                                json.loads(
                                    json.dumps({
                                        "data" : "Instance has been activated successfully"
                                    })
                                ),
                                status =200
                            )
                        else:
                            print("--> PENSTACK SAVE DOMAIN CLIENT FLAGS TO LOCAL DB REQUEST STARTED")
                            print(response.content)
                            return JsonResponse(
                                json.loads(
                                    json.dumps({

                                        "error" : str( response.json()["error"]["message"] )
                                    })
                                ),
                                status =400
                            )
                    else:
                        print("--> OPENSTACK GET DOMAIN CLIENT PUBLIC IP REQUEST ERROR")
                        print(response.content)
                        return JsonResponse(
                            json.loads(
                                json.dumps({

                                    "error" : str( response.json()["error"]["message"] )
                                })
                            ),
                            status =400
                        )
                    # return JsonResponse(
                    #     json.loads(
                    #         json.dumps({
                    #             "data" : "Instance has been started successfully"
                    #         })
                    #     ),
                    #     status =200
                    # )
            else:
                print("--> OPENSTACK DETAILS DOMAIN CLIENT REQUEST ERROR")
                print(response.content)
                return JsonResponse(
                    json.loads(
                        json.dumps({

                            "error" : str( response.json()["error"]["message"] )
                        })
                    ),
                    status =400
                )
        else:
            print("--> OPENSTACK AUTHENTICATION ERROR")
            print(response.content)
            return JsonResponse(
                json.loads(
                    json.dumps({

                        "error" : str( response.json()["error"]["message"] )
                    })
                ),
                status =400
            )

    except Exception as e:
        print("--> EXCEPTION OCCURED")
        traceback.print_exc() 
        return JsonResponse(
            json.loads(
                json.dumps({
                    "error" : str(e)
                })
            ),
            status =400
        )


# TODO  :   # ? Create an instance in openstack for requested virtual image
def AdminCreateNetworkInstance(request, vn_id):
    try:
        netObj = VirtualNetwork.objects.get(id = vn_id)
        headers = {
            'Content-Type': 'application/json',
        }
        json_data = {
        'auth': {
            'identity': {
                'methods': [
                    'password',
                ],
                'password': {
                    'user': {
                        'name': settings.OPENSTACK_USER,
                        'domain': {
                            'id': 'default',
                        },
                        'password': settings.OPENSTACK_PASSWORD,
                    },
                },
            },
            "scope": {
            "project": {
            "name": "admin",
            "domain": { "id": "default" }
            }
        }
            
        },
        }

        s = requests.Session()
        print("--> OPENSTACK SESSION STARTED")
        response = s.post(settings.OPENSTACK_AUTHORIZED_URL, headers=headers, json=json_data)
        print("--> OPENSTACK AUTHORIZATION STARTED")
        if response.status_code in [200, 201, 202]:
            # print("--> OPENSTACK AUTHORIZATION SUCCESSFUL")
            headers = {
                'X-Auth-Token': f'{response.headers["x-subject-token"]}',   
            }
            json_data={
                "server": {
                    "name": f"{netObj.name}",
                    "imageRef": f"{netObj.imageRef}",
                    "flavorRef": settings.OPENSTACK_FLAVOR_URL,
                    "networks": [{
                        "uuid" : settings.OPENSTACK_NETWORK_UUID
                    }]
                }
            }
            print("--> OPENSTACK CREATE SERVER INSTANCE REQUEST STARTED")
            response = s.post(settings.OPENSTACK_SERVER_URL, headers=headers , json=json_data)
            if response.status_code in [200, 201, 202]:
                # print("--> OPENSTACK CREATE SERVER INSTANCE REQUEST SUCCESSFUL")
                netObj.server_id = response.json()["server"]["id"]
                netObj.save()
                print("--> OPENSTACK FLOATING IP REQUEST STARTED")
                response = s.get(settings.OPENSTACK_FLOATING_IP_URL, headers=headers)
                if response.status_code in [200, 201, 202]:
                    floating_ip = None
                    for i in response.json()['floating_ips']:
                        if i["instance_id"] == None and i["pool"] == settings.OPENSTACK_NETWORK_POOL:  
                            floating_ip = i["ip"]
                            break
                    if floating_ip:
                        print("--> OPENSTACK FLOATING IP EXISTS TO ASSOCIATE")
                        print("--> OPENSTACK ASSIGNED FLOATING IP REQUEST STARTED")
                        json_data = {
                            "addFloatingIp" : {
                                "address": floating_ip
                            }
                        }
                        # TODO :    extra time to request
                        time.sleep(10)
                        response = s.post(f'{settings.OPENSTACK_SERVER_URL}/{netObj.server_id}/action', headers=headers , json=json_data)
                        if (response.status_code in [200, 201, 202]):
                            netObj.ip_address = floating_ip
                            netObj.save()
                            # print("--> OPENSTACK ASSIGNED FLOATING IP REQUEST SUCCESSFUL")
                            netObj.is_instance_created = True
                            netObj.save()

                            # TODO :    extra time to request
                            # time.sleep(15)

                            # TODO : Spawn DC
                            if settings.IS_SPAWN_DC is True:
                                print("--> DC : OPENSTACK SPAWN DC")
                                json_data={
                                    "server": {
                                        "name": f"{netObj.name} DC",
                                        "imageRef": settings.OPENSTACK_DC_UUID,
                                        "flavorRef": settings.OPENSTACK_FLAVOR_URL,
                                        "networks": [{
                                            "uuid" : settings.OPENSTACK_NETWORK_UUID
                                        }]
                                    }
                                }
                                print("--> DC : OPENSTACK SPAWN REQUEST STARTED")
                                response = s.post(settings.OPENSTACK_SERVER_URL, headers=headers , json=json_data)
                                if response.status_code in [200, 201, 202]:
                                    print("--> DC : OPENSTACK DC REQUEST SUCCESSFUL")
                                    dc_server_id = response.json()["server"]["id"]

                                    print("--> DC : OPENSTACK FLOATING IP  REQUEST STARTED")
                                    response = s.get(settings.OPENSTACK_FLOATING_IP_URL, headers=headers)
                                    if response.status_code in [200, 201, 202]:
                                        floating_ip = None
                                        for i in response.json()['floating_ips']:
                                            if i["instance_id"] == None and i["pool"] == settings.OPENSTACK_NETWORK_POOL:  
                                                floating_ip = i["ip"]
                                                break
                                        if floating_ip:
                                            print("--> DC : OPENSTACK FLOATING IP ALREADY EXISTS TO ASSOCIATE")
                                            print("--> DC : OPENSTACK ASSIGNED FLOATING IP REQUEST STARTED")
                                            time.sleep(10)
                                            json_data = {
                                                "addFloatingIp" : {
                                                    "address": floating_ip
                                                }
                                            }
                                            response = s.post(f'{settings.OPENSTACK_SERVER_URL}/{dc_server_id}/action', headers=headers , json=json_data)
                                            if (response.status_code in [200, 201, 202]):
                                                print("--> DC : OPENSTACK ASSIGNED FLOATING IP  REQUEST SUCCESSFUL")
                                            else:
                                                print("--> DC : OPENSTACK ASSIGNED FLOATING IP  REQUEST ERROR")
                                                print(response.content)
                                        else:
                                            print("--> DC : OPENSTACK FLOATING IP REQUEST STARTED")
                                            json_data={
                                                "pool": settings.OPENSTACK_NETWORK_POOL
                                            }
                                            response  =s.post(settings.OPENSTACK_FLOATING_IP_URL, headers=headers , json=json_data)

                                            # TODO :    extra time to request
                                            # time.sleep(10)

                                            if response.status_code in [200, 201, 202]:
                                                print("--> DC : OPENSTACK FLOATING IP REQUEST SUCCESSFUL")
                                                json_data = {
                                                    "addFloatingIp" : {
                                                        "address": response.json()["floating_ip"]["ip"]
                                                    }
                                                }

                                                # TODO :    extra time to request
                                                time.sleep(10)

                                                print("--> DC : OPENSTACK ASSIGNED FLOATING IP REQUEST STARTED")
                                                response = s.post(f'{settings.OPENSTACK_SERVER_URL}/{dc_server_id}/action', headers=headers , json=json_data)
                                                if (response.status_code in [200, 201, 202]):
                                                    print("--> DC : OPENSTACK ASSIGNED FLOATING IP REQUEST SUCCESSFUL")
                                                else:
                                                    print("--> DC : OPENSTACK ASSIGNED FLOATING IP REQUEST ERROR")
                                                    print(response.content)
                                            else:
                                                print("--> DC : OPENSTACK FLOATING IP REQUEST ERROR")
                                                print(response.content)
                                    else:
                                        print("--> DC : OPENSTACK FLOATING IP REQUEST ERROR")
                                        print(response.content)
                                else:
                                    print("--> DC : OPENSTACK SPAWN REQUEST ERROR")
                                    print(response.content)

                            # TODO :    save flags to local database
                            try:
                                time.sleep(3)
                                print("--> SAVE FLAGS FOR CURRENT INSTANCE TO LOAD DB")
                                response = s.get(f'{settings.OPENSTACK_IMAGE_URL}/{netObj.imageRef}', headers=headers )
                                if response.status_code in [200, 201, 202]:
                                    for i in response.json():
                                        if i[:4].lower() == "flag":
                                            try:
                                                netFlag = NetworkFlag.objects.get_or_create(
                                                    course = netObj.course,
                                                    flag_id = i
                                                )
                                                netFlag[0].original_answer = response.json()[i]
                                                netFlag[0].points = 50
                                                netFlag[0].imageRef = netObj.imageRef
                                                netFlag[0].save()
                                            except Exception as e:
                                                print("--> EXCEPTION OCCURED")
                                                traceback.print_exc() 
                                    print("--> SAVE FLAGS FOR CURRENT INSTANCE TO LOAD DB SUCCESSFUL")
                                else:
                                    print("--> SAVE FLAGS FOR CURRENT INSTANCE TO LOAD DB ERROR")
                                    print(response.content)
                            except Exception as e:
                                print("--> EXCEPTION OCCURED")
                                traceback.print_exc() 
                            return JsonResponse(
                                json.loads(
                                    json.dumps({
                                        "data" : "Instance has been created successfully"
                                    })
                                ),
                                status =200
                            )
                        else:
                            print("--> OPENSTACK ASSIGNED FLOATING IP REQUEST ERROR")
                            print(response.content)
                            if(response.status_code == 400):
                                return JsonResponse(
                                    json.loads(
                                        json.dumps({
                                            "error" : str( response.json()["badRequest"]["message"] )
                                        })
                                    ),
                                    status =400
                                )        
                            else:
                                return JsonResponse(
                                    json.loads(
                                        json.dumps({
                                            "error" : str( response.json()["error"]["message"] )
                                        })
                                    ),
                                    status =400
                                )
                    else:
                        print("--> OPENSTACK CREATE NEW FLOATING IP REQUEST START")
                        json_data={
                            "pool": settings.OPENSTACK_NETWORK_POOL
                        }
                        response  =s.post(settings.OPENSTACK_FLOATING_IP_URL, headers=headers , json=json_data)
                        if response.status_code in [200, 201, 202]:
                            # print("--> OPENSTACK CREATE NEW FLOATING IP REQUEST SUCCESSFUL")
                            netObj.ip_address = response.json()["floating_ip"]["ip"]
                            netObj.save()
                            json_data = {
                                "addFloatingIp" : {
                                    "address": response.json()["floating_ip"]["ip"]
                                }
                            }
                            # TODO :    extra time to request
                            time.sleep(10)

                            print("--> OPENSTACK ASSIGNED FLOATING IP REQUEST STARTED")
                            response = s.post(f'{settings.OPENSTACK_SERVER_URL}/{netObj.server_id}/action', headers=headers , json=json_data)
                            if (response.status_code in [200, 201, 202]):
                                print("--> OPENSTACK ASSIGNED FLOATING IP REQUEST SUCCESSFUL")
                                netObj.is_instance_created = True
                                netObj.save()

                                # TODO :    extra time to request
                                # time.sleep(15)

                                # TODO : Spawn DC
                                if settings.IS_SPAWN_DC is True:
                                    json_data={
                                        "server": {
                                            "name": f"{netObj.name} DC",
                                            "imageRef": settings.OPENSTACK_DC_UUID,
                                            "flavorRef": settings.OPENSTACK_FLAVOR_URL,
                                            "networks": [{
                                                "uuid" : settings.OPENSTACK_NETWORK_UUID
                                            }]
                                        }
                                    }
                                    print("--> DC : OPENSTACK SPAWN REQUEST STARTED")
                                    response = s.post(settings.OPENSTACK_SERVER_URL, headers=headers , json=json_data)
                                    if response.status_code in [200, 201, 202]:
                                        print("--> DC : OPENSTACK SPAWN REQUEST SUCCESSFUL")
                                        dc_server_id = response.json()["server"]["id"]

                                        print("--> DC : OPENSTACK FLOATING IP REQUEST STARTED")
                                        response = s.get(settings.OPENSTACK_FLOATING_IP_URL, headers=headers)
                                        if response.status_code in [200, 201, 202]:
                                            floating_ip = None
                                            for i in response.json()['floating_ips']:
                                                if i["instance_id"] == None and i["pool"] == settings.OPENSTACK_NETWORK_POOL:  
                                                    floating_ip = i["ip"]
                                                    break
                                            if floating_ip:
                                                print("--> DC : OPENSTACK FLOATING IP ALREADY EXISTS")
                                                # TODO :    extra time to request
                                                # time.sleep(10)
                                                print("--> DC : OPENSTACK ASSIGNED FLOATING IP  STARTED")
                                                json_data = {
                                                    "addFloatingIp" : {
                                                        "address": floating_ip
                                                    }
                                                }
                                                response = s.post(f'{settings.OPENSTACK_SERVER_URL}/{dc_server_id}/action', headers=headers , json=json_data)
                                                if (response.status_code in [200, 201, 202]):
                                                    print("--> DC : OPENSTACK ASSIGNED FLOATING IP REQUEST SUCCESSFUL")
                                                else:
                                                    print("--> DC : OPENSTACK ASSIGNED FLOATING IP REQUEST ERROR")
                                                    print(response.content)
                                            else:
                                                print("--> DC : OPENSTACK CREATE NEW FLOATING IP REQUEST STARTED")
                                                json_data={
                                                    "pool": settings.OPENSTACK_NETWORK_POOL
                                                }
                                                response  =s.post(settings.OPENSTACK_FLOATING_IP_URL, headers=headers , json=json_data)

                                                # TODO :    extra time to request
                                                # time.sleep(15)

                                                if response.status_code in [200, 201, 202]:
                                                    print("--> DC : OPENSTACK CREATE NEW FLOATING IP REQUEST SUCCESSFUL")
                                                    json_data = {
                                                        "addFloatingIp" : {
                                                            "address": response.json()["floating_ip"]["ip"]
                                                        }
                                                    }

                                                    # TODO :    extra time to request
                                                    time.sleep(10)

                                                    print("--> DC : OPENSTACK ASSIGNED FLOATING IP REQUEST STARTED")
                                                    response = s.post(f'{settings.OPENSTACK_SERVER_URL}/{dc_server_id}/action', headers=headers , json=json_data)
                                                    if (response.status_code in [200, 201, 202]):
                                                        print("--> DC : OPENSTACK ASSIGNED FLOATING IP REQUEST SUCCESSFUL")
                                                    else:
                                                        print("--> DC : OPENSTACK ASSIGNED FLOATING IP REQUEST ERROR")
                                                        print(response.content)
                                                else:
                                                    print("--> DC : OPENSTACK CREATE NEW FLOATING IP REQUEST ERROR")
                                                    print(response.content)
                                        else:
                                            print("--> DC : OPENSTACK FLOATING IP REQUEST ERROR")
                                            print(response.content)
                                    else:
                                        print("--> DC : OPENSTACK SPAWN REQUEST ERROR")
                                        print(response.content)

                                
                                    
                                    
                                    # TODO :    save flags to local database
                                    try:
                                        time.sleep(3)
                                        print("--> SAVE FLAGS FOR CURRENT INSTANCE TO LOAD DB")
                                        response = s.get(f'{settings.OPENSTACK_IMAGE_URL}/{netObj.imageRef}', headers=headers )
                                        if response.status_code in [200, 201, 202]:
                                            for i in response.json():
                                                if i[:4].lower() == "flag":
                                                    try:
                                                        netFlag = NetworkFlag.objects.get_or_create(
                                                            course = netObj.course,
                                                            flag_id = i
                                                        )
                                                        netFlag[0].original_answer = response.json()[i]
                                                        netFlag[0].points = 50
                                                        netFlag[0].imageRef = netObj.imageRef
                                                        netFlag[0].save()
                                                    except Exception as e:
                                                        print("--> EXCEPTION OCCURED")
                                                        traceback.print_exc() 
                                            print("--> SAVE FLAGS FOR CURRENT INSTANCE TO LOAD DB SUCCESSFUL")
                                        else:
                                            print("--> SAVE FLAGS FOR CURRENT INSTANCE TO LOAD DB ERROR")
                                            print(response.content)
                                    except Exception as e:
                                        print("--> EXCEPTION OCCURED")
                                        traceback.print_exc() 
                                    return JsonResponse(
                                        json.loads(
                                            json.dumps({
                                                "data" : "Instance has been created successfully"
                                            })
                                        ),
                                        status =200
                                    )
                            
                                # TODO :    save flags to local database
                                try:
                                    time.sleep(3)
                                    print("--> SAVE FLAGS FOR CURRENT INSTANCE TO LOAD DB")
                                    response = s.get(f'{settings.OPENSTACK_IMAGE_URL}/{netObj.imageRef}', headers=headers )
                                    if response.status_code in [200, 201, 202]:
                                        for i in response.json():
                                            if i[:4].lower() == "flag":
                                                try:
                                                    netFlag = NetworkFlag.objects.get_or_create(
                                                        course = netObj.course,
                                                        flag_id = i
                                                    )
                                                    netFlag[0].original_answer = response.json()[i]
                                                    netFlag[0].points = 50
                                                    netFlag[0].imageRef = netObj.imageRef
                                                    netFlag[0].save()
                                                except Exception as e:
                                                    print("--> EXCEPTION OCCURED")
                                                    traceback.print_exc() 
                                        print("--> SAVE FLAGS FOR CURRENT INSTANCE TO LOAD DB SUCCESSFUL")
                                    else:
                                        print("--> SAVE FLAGS FOR CURRENT INSTANCE TO LOAD DB ERROR")
                                        print(response.content)
                                except Exception as e:
                                    print("--> EXCEPTION OCCURED")
                                    traceback.print_exc() 
                                return JsonResponse(
                                    json.loads(
                                        json.dumps({
                                            "data" : "Instance has been created successfully"
                                        })
                                    ),
                                    status =200
                                )
                            
                            else:
                                print("--> OPENSTACK ASSIGNED FLOATING IP REQUEST ERROR")
                                print(response.content)
                                if response.status_code == 400:
                                    return JsonResponse(
                                        json.loads(
                                            json.dumps({
                                                "error" : str( response.json()["badRequest"]["message"] )
                                            })
                                        ),
                                        status =400
                                    )
                                else:
                                    return JsonResponse(
                                        json.loads(
                                            json.dumps({
                                                "error" : str( response.json()["error"]["message"] )
                                            })
                                        ),
                                        status =400
                                    )

                        else:
                            print("--> OPENSTACK FLOATING IP REQUEST ERROR")
                            print(response.content)
                            return JsonResponse(
                                json.loads(
                                    json.dumps({
                                        "error" : str( response.json()["error"]["message"] )
                                    })
                                ),
                                status =400
                            )
                else:
                    print("--> OPENSTACK FLOATING IP REQUEST ERROR")
                    print(response.content)
                    return JsonResponse(
                        json.loads(
                            json.dumps({
                                "error" : str( response.json()["error"]["message"] )
                            })
                        ),
                        status =400
                    )
            else:
                print("--> OPENSTACK CREATE NEW SERVER INSTANCE REQUEST ERROR")
                print(response.content)
                return JsonResponse(
                    json.loads(
                        json.dumps({
                            "error" : str(response.json()["error"]["message"])
                        })
                    ),
                    status =400
                )
        else:
            print("--> OPENSTACK AUTHENTICATION ERROR")
            print(response.content)
            return JsonResponse(
                json.loads(
                    json.dumps({

                        "error" : str( response.json()["error"]["message"] )
                    })
                ),
                status =400
            )
    except Exception as e:
        print("--> EXCEPTION OCCURED")
        traceback.print_exc() 
        return JsonResponse(
            json.loads(
                json.dumps({
                    "error" : str(e)
                })
            ),
            status =400
        )


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
        
    # # TODO  :   Retrieve All Instructors
    # instructors = User.objects.filter(is_instructor = True)
    
    # TODO  :   Retrieve All Courses
    courses = Course.objects.filter(instructor__id = request.user.id).order_by("-created_timestamp")
    # print(courses)

    # TODO  :   Retrieve All Students to that instructor
    students=[]
    for course in courses:
        for student in course.assignedstudents_set.all():
            students.append(student.student)


    # TODO  :   Retrieve All Local Virutal Networks to that instructor
    networks=[]
    for course in courses:
        for network in course.virtualnetwork_set.all():
            networks.append(network)

    # print(networks)

    # TODO  :   Recent Acitivty 
    # entries = LogEntry.objects.all()
    
    context = {
        # "instructors"  : instructors,
        "students" : students,
        "courses" : courses,
        "networks" : networks,
        # "entries" : entries
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
    all_courses = Course.objects.filter(instructor=request.user).order_by("-id")

    # print(all_courses)
    context = {
        "all_courses": all_courses
    }
    return render(request, template_name, context)



# TODO  :   Instructor Students Lists
@login_required
@teacher_required
def StudentList(request):
    template_name = 'master_app/instructor/student_list.html'
    # TODO  :   Retrieve All Instructor Courses
    all_students = User.objects.filter(is_student = True)
    # all_courses = Course.objects.filter(instructor=request.user)

    # TODO  :   Retrieve All Students
    # all_students = []
    # for i in all_courses:
    #     all_students.append(i.assignedstudents_set.all())
    context = {
        "all_students": all_students
    }
    return render(request, template_name, context)


# TODO  :   Instructor Create Student
@login_required
@teacher_required
def InstructorCreateStudent(request):
    template_name="master_app/instructor/student_create.html"
    if request.method!='POST':
            form = registerForm()
    else:
        form = registerForm(request.POST)
        if form.is_valid() :
            user = form.save(commit=False)
            user.is_active = True
            user.is_student = True
            user.set_password(form.cleaned_data['password2'])
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.save()
            messages.success(request, "New Student has been created")
            return redirect(reverse("students-all-url"))
    context={
        'form' : form
    }
    return render(request, template_name, context)


# TODO  :   Instructor Create New Course
@login_required
@teacher_required
def CreateCourse(request):
    template_name = 'master_app/instructor/create_course.html'
    if request.method == "POST":
        form = CreateCourseForm(request.POST ,  request.FILES)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.instructor = request.user
            new_course.save()
            return redirect(reverse("instructor-courses-details-url", args=[new_course.id]))
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
        "WAZUH_SERVER_PUBLIC_IP" : settings.WAZUH_SERVER_PUBLIC_IP,
        "DC_IP_ADDRESS" : settings.DC_IP_ADDRESS
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
    # print(request.POST)
    if request.method == "POST" :
        form = NewVirtualNetworkForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse(
                json.loads(
                    json.dumps({
                        "text" : "Valid method"
                    })
                ),
                status =200
            )
        else:
            # print(form.errors)
            return JsonResponse(
            json.loads(
                json.dumps({
                    "error" : json.dumps(form.errors)
                })
            ),
            status =400
        )
        
    else:
        return JsonResponse(
            json.loads(
                json.dumps({
                    "error" : "Invalid request method"
                })
            ),
            status =400
        )
    # ===========================
    # Oiginal code
    # template_name = 'master_app/instructor/virutal_netwroks_new.html'
    # if request.method == "POST":
    #     form = NewVirtualNetworkForm(request.POST)
    #     # print(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, "New Network Machine Has been added")
    #         if request.POST.get("next", None):
    #             return redirect(request.POST.get("next", None))
    #         return redirect(reverse("instructor-virtual-network-url"))
    # else:
    #     form = NewVirtualNetworkForm()
    # context = {
    #     "form": form
    # }
    # return render(request, template_name, context)
    # ============================================

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
    if request.method == "POST" :
        # print(request.POST)
        form = AddNewStudent(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse(
                json.loads(
                    json.dumps({
                        "text" : "New Student has been added",
                        "next" : request.POST.get("next", None)
                    })
                ),
                status =200
            )
        else:
            return JsonResponse(
            json.loads(
                json.dumps({
                    "error" : json.dumps(form.errors)
                })
            ),
            status =400
        )
        
    else:
        return JsonResponse(
            json.loads(
                json.dumps({
                    "error" : "Invalid request"
                })
            ),
            status =400
        )
# =====================
    # Original Code
    # template_name = 'master_app/instructor/add_new_student.html'
    # if request.method == "POST":
    #     form = AddNewStudent(request.POST)
    #     # print(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, "New Student has been added")
    #         if request.POST.get("next", None):
    #             return redirect(request.POST.get("next", None))
    #         return redirect(reverse("students-all-url"))
    #     # else:
    #     #     print(form.errors)
    #     #     messages.error(request, str())

    # else:
    #     form = AddNewStudent()
    # context = {
    #     "form": form
    # }
    # return render(request, template_name, context)
# ===================



# TODO  :   Student Dashboard
@login_required
@student_required
def StudentDashboard(request):
    template_name = 'master_app/student/dashboard.html'
    
    # TODO  :   Retrieve All Courses Active 
    courses = [x for x in AssignedStudents.objects.filter(student__id = request.user.id).order_by("-created_timestamp") if x.course.is_course_approved()]

    # TODO  :   Retrieve All Local Virutal Networks to that student
    networks=[]
    for course in courses:
        for network in course.course.virtualnetwork_set.all():
            networks.append(network)
    
    context = {
        "courses" : courses,
        "networks" : networks,
    }
    return render(request, template_name, context)


# TODO  :   Student Courses
@login_required
@student_required
def StudentCourses(request):
    template_name = 'master_app/student/courseList.html'
    courses = AssignedStudents.objects.filter(
        student__id=request.user.id
        ).filter(
            course__is_approved="3"
        ).order_by(
            '-id'
        )
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
        wazuh_server_ip = settings.WAZUH_SERVER_PUBLIC_IP
    except:
        messages.error(request, "Requested course does not exist")
        return redirect(reverse("student-courses-url"))

    context = {
        "course": course,
        "easy_challenges": easy_challenges,
        "medium_challenges": medium_challenges,
        "hard_challenges": hard_challenges,
        "wazuh_server_ip" : wazuh_server_ip,
        "WAZUH_SERVER_PASSWORD" : settings.WAZUH_SERVER_PASSWORD
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




def StudentFlagSubmission(request):
    # print(request.POST)
    customPrint(request.POST)
    if request.method == "POST" :
        try:
            netFlag = NetworkFlag.objects.get(
                course__id = request.POST['course_id'],
                flag_id = request.POST['flag_id']
            )
            student = AssignedStudents.objects.get(
                course__id = request.POST['course_id'],
                student__id = request.user.id
            )
            subObj = NetworkFlagSubmission.objects.get_or_create(
                student = student,
                flag_id = netFlag.flag_id
            )
            if(subObj[0].submit_status != 1):
                subObj[0].attemptUsed = subObj[0].attemptUsed + 1
                subObj[0].submittedAnswer = request.POST.get("flag", None)
                subObj[0].save()
                if netFlag.original_answer == request.POST.get("flag", None):
                    subObj[0].obtainedPoints = netFlag.points
                    subObj[0].status = "SUBMITTED"
                    subObj[0].save()
                    try:
                        LogEntry.objects.create(
                            user = request.user,
                            action_flag=ADDITION,
                            object_id=request.user.id,
                            content_type_id=get_content_type_for_model(request.user).pk,
                            object_repr=force_str(request.user),
                            change_message = f"{request.user} has successfully submitted flag for {netFlag.course}."
                        )
                    except Exception as e:
                        print(e)
                    return JsonResponse(
                        json.loads(
                            json.dumps({
                                "text" : "Flag has been submitted successfully"
                            })
                        ),
                        status =200
                    )
                else:
                    try:
                        LogEntry.objects.create(
                            user = request.user,
                            action_flag=ADDITION,
                            object_id=request.user.id,
                            content_type_id=get_content_type_for_model(request.user).pk,
                            object_repr=force_str(request.user),
                            change_message = f"{request.user} has submitted wrong flag for {netFlag.course}."
                        )
                    except Exception as e:
                        print(e)
                    return JsonResponse(
                        json.loads(
                            json.dumps({
                                "error" : "Wrong Flag Submission"
                            })
                        ),
                        status =400
                    )
            else:
                return JsonResponse(
                    json.loads(
                        json.dumps({
                            "error" : "Flag already has been submitted"
                        })
                    ),
                    status =400
                )
        except Exception as e:
            customPrint(e)
            return JsonResponse(
                json.loads(
                    json.dumps({
                        "error" : "Invalid Flag Submission."
                    })
                ),
                status =400
            )
    else:
        return JsonResponse(
            json.loads(
                json.dumps({
                    "error" : "Invalid request method"
                })
            ),
            status =400
        )

# # orignal_code
# def StudentFlagSubmission(request):
#     if request.method == "POST" :
        
#         # print(request.POST)

#         try:
#             netObj = VirtualNetwork.objects.get(id = request.POST["vn_id"])

#             # ======open stack authentiation======

#             headers = {
#                 'Content-Type': 'application/json',
#             }

#             json_data = {
#             'auth': {
#                 'identity': {
#                     'methods': [
#                         'password',
#                     ],
#                     'password': {
#                         'user': {
#                             'name': 'admin',
#                             'domain': {
#                                 'id': 'default',
#                             },
#                             'password': 'password',
#                         },
#                     },
#                 },
#                 "scope": {
#                 "project": {
#                 "name": "admin",
#                 "domain": { "id": "default" }
#                 }
#             }
                
#             },
#             }

#             s = requests.Session()
#             response = s.post('http://10.1.2.9:5000/v3/auth/tokens', headers=headers, json=json_data)
#             # print(response.json())

#             if response.status_code == 201:
#                 # print(response.headers["x-subject-token"])
#                 headers = {
#                     'X-Auth-Token': f'{response.headers["x-subject-token"]}',
                    
#                 }

#                 time.sleep(2)

#                 # fetch images from open stack
#                 response = s.get(f'http://10.1.2.9:9292/v2/images/{netObj.imageRef}', headers=headers )

#                 # print(response.status_code)

#                 if response.status_code == 200:
#                     # print(response.text)
#                     # with open('data.json', 'w') as f:
#                     #     json.dump(response.text, f)
#                     # with open('data.json', 'w', encoding='utf-8') as f:
#                     #     json.dump(response.json(), f, ensure_ascii=False, indent=4)
#                     if request.POST.get("Flag 1", None):
#                         flag_1 = response.json()["Flag 1"]
#                         # print(flag_1)
#                         if( request.POST["Flag 1"]  == flag_1):
#                             return JsonResponse(
#                                 json.loads(
#                                     json.dumps({
#                                         "data" : response.json()
#                                     })
#                                 ),
#                                 status =200
#                             )
#                         else:
#                             return JsonResponse(
#                             json.loads(
#                                 json.dumps({
#                                     "error" : "Invalid Flag Submit"
#                                 })
#                             ),
#                             status = 400
#                         )
                    
#                     elif request.POST.get("Flag 2", None):
#                         flag_2 = response.json()["Flag 2"]
#                         # print(flag_2)
#                         if( request.POST["Flag 2"]  == flag_2):
#                             return JsonResponse(
#                                 json.loads(
#                                     json.dumps({
#                                         "data" : response.json()
#                                     })
#                                 ),
#                                 status =200
#                             )
#                         else:
#                             return JsonResponse(
#                             json.loads(
#                                 json.dumps({
#                                     "error" : "Invalid Flag Submit"
#                                 })
#                             ),
#                             status = 400
#                         )
#                     else:
#                         return JsonResponse(
#                         json.loads(
#                             json.dumps({
#                                 "error" : "Invalid Flag Submit"
#                             })
#                         ),
#                         status = 400
#                     )
                
                            

                    
#                 else:
#                     return JsonResponse(
#                     json.loads(
#                         json.dumps({
#                             "error" : "Error in validating flag."
#                         })
#                     ),
#                     status = 400
#                 )

#             return JsonResponse(
#             json.loads(
#                 json.dumps({
#                     "text" : "Valid Submissoin"
#                 })
#             ),
#             status =200
#         )
#         except:
#             return JsonResponse(
#             json.loads(
#                 json.dumps({
#                     "error" : "Invalid flag submission. Please Try Again."
#                 })
#             ),
#             status =400
#         )

        
        
#     else:
#         return JsonResponse(
#             json.loads(
#                 json.dumps({
#                     "error" : "Invalid request "
#                 })
#             ),
#             status =400
#         )



def ContactView(request):
    template_name = 'master_app/contact.html'
    context = {
    }
    return render(request, template_name, context)


def AboutView(request):
    template_name = 'master_app/about.html'
    context = {
    }
    return render(request, template_name, context)

@login_required
def CreateVPN(request):
    try:
        filename = str(uuid.uuid4())
        exe_path = f"{settings.BASE_DIR / 'openvpngen.sh'}"
        output_path = settings.MEDIA_ROOT / f'{filename}.ovpn'
        try:
            subprocess.Popen(['sudo', '-S',  exe_path, filename], stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True).communicate(settings.OPENSTACK + '\n')[1]
        except:
            print("="*50)
            traceback.print_exc()
            print("="*50)
        if request.method == "GET" :
            # TODO  :   Retrieve Current user object
            try:
                current_user = User.objects.get(id = request.user.id)
                if current_user.vpn_file:
                    return JsonResponse(
                        json.loads(
                            json.dumps({
                                "error" : "Already File Generated."
                            })
                        ),
                        status =400
                    )
                else:
                    current_user.vpn_file.save(f"{filename}.ovpn", File(open(output_path)))
                    if os.path.exists(output_path):
                       os.remove(output_path)
                    return JsonResponse(
                        json.loads(
                            json.dumps({
                                 "text" : "created" 
                            })
                        ),
                        status =200
                    )
            except Exception as e:
                print("="*50)
                traceback.print_exc()
                print("="*50)
                return JsonResponse(
                    json.loads(
                        json.dumps({
                            "error" : "Please try again after sometime"
                        })
                    ),
                    status =400
                )
        else:
            return JsonResponse(
                json.loads(
                    json.dumps({
                        "error" : "Invalid request method"
                    })
                ),
                status =400
            )
    except :
        print("="*50)
        traceback.print_exc()
        print("="*50)
        return JsonResponse(
            json.loads(
                json.dumps({
                    "error" : "Please try again after sometime"
                })
            ),
            status =400
        )





# sudo systemctl daemon-reload
# sudo systemctl restart gunicorn
# sudo systemctl restart nginx
# sudo journalctl -u gunicorn
# sudo chmod -R 777 ./crfront/
# cyber-range.rocks

# /home/openstack/backups/22/cys_games/db.sqlite3
# /home/openstack/crfront/cys_games/db.sqlite3

# /home/openstack/backups/22/media
# /home/openstack/crfront/media