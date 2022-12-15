from django.urls import path

from . import views


urlpatterns = [
    # ? Home Route
    path('', views.index , name="master_index"),

    # ? User Login Route
    path('login/', views.UserLoginView, name="user-login"),

    # ? User login (Ajax)
    path('login-ajax/', views.UserLoginAjaxView, name="user-login-ajax"),

    # ? User Logout Route
    path('logout/', views.UserLogoutView, name="user-logout"),


    # ==========================================================
    # ? Admin Dashbaord
    path("admin/", views.AdminDashboard, name="admin-dasboard-url"),

    # ? Admin Profile
    path("admin/profile", views.AdminProfile, name="admin-profile-url"),


    # ==========================================================
    # ? Instructor Dashbaord
    path("instructor/", views.InstructorDashboard, name="instructor-dasboard-url"),

    # ? Instructor Profile
    path("instructor/profile", views.InsturctorProfile, name="instructor-profile-url"),
    

    # ? Instructor Create New Virtual Network
    path("instructor/virtual-network/create/new" , views.InstructorVirturalNetworkNew, name="instructor-virutal-network-create-url"),

    # ? Instructor Virutal Networks
    path("instructor/virtaul-networks", views.InstructorVirtualNetworkList, name="instructor-virtual-network-url"),

    # ? Instructor Courses List
    path("instructor/courses", views.CoursesList, name="courses-all-url"),

    # ? Instructor Courses Detials
    path("instructor/courses/<int:course_id>/details", views.InstructorCourseDetails, name="instructor-courses-details-url"),

    # ? Instructor Students List
    path("instructor/students", views.StudentList, name="students-all-url"),

    # ? Instructor Create New Course
    path("instructor/course/new", views.CreateCourse, name="course-new-url"),

    # ? Instructor Create New Challenge
    path("instructor/course/challenge/new", views.InstructorCreateNewChallenge, name="instructor-create-new-challenge-url"),

    

    # ? Instructor Add New Student
    path("instructor/course/students/new", views.AddNewStudents, name="course-students-new-url"),

    


    # ==========================================================
    # ? Student Dashbaord
    path("student/", views.StudentDashboard, name="student-dasboard-url"),
    
    # ? Student Profile
    path("student/profile", views.StudentProfile, name="student-profile-url"),

    # ? Student Courses
    path("student/courses", views.StudentCourses, name="student-courses-url"),

    # ? Student Courses Detials
    path("student/courses/details", views.StudentCourseDetails, name="student-courses-details-url"),

    # ? Student Machines
    path("student/machines", views.StudentMachines, name="student-machines-url"),
    
    # ? Student Machine Details
    path("student/machine/detail", views.StudentMachineDetail, name="student-machine-detail-url"),

]

