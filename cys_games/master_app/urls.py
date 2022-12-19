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
    path("admininstrator/", views.AdminDashboard, name="admin-dasboard-url"),

    # ? Admin Profile
    path("admininstrator/profile", views.AdminProfile, name="admin-profile-url"),

    # ? Admin Course List
    path("admininstrator/course/all", views.AdminCourseList, name="admin-course-list-url"),

    # ? Admin Create New Course
    path("admininstrator/course/new", views.AdminCreateCourse, name="admin-course-new-url"),
    
    # ? Admin Course Details
    path("admininstrator/course/<int:course_id>/details", views.AdminCourseDetails, name="admin-courses-details-url"),

    # ? Admin Course Approval Form Submission
    path("admininstrator/course/<int:vn_id>/approval", views.AdminCourseApproval, name="admin-course-approval-url"),

    # ? Admin Course Reject
    path("admininstrator/course/<int:course_id>/reject", views.AdminCourseReject, name="admin-course-reject-url"),

    # ? Admin Virutal Networks
    path("admin/virtaul-networks", views.AdminVirtualNetworkList, name="admin-virtual-network-url"),

    # ? Admin Virutal Networks Details
    path("admin/virtaul-networks/<int:vn_id>/detail", views.AdminVirtualNetworkDetails, name="admin-machine-detail-url"),


    # ==========================================================
    # ? Instructor Dashbaord
    path("instructor/", views.InstructorDashboard, name="instructor-dasboard-url"),

    # ? Instructor Profile
    path("instructor/profile", views.InsturctorProfile, name="instructor-profile-url"),
    
    # ? Instructor Create New Course
    path("instructor/course/new", views.CreateCourse, name="course-new-url"),

    # ? Instructor Add New Student
    path("instructor/course/students/new", views.AddNewStudents, name="course-students-new-url"),

    # ? Instructor Create New Challenge
    path("instructor/course/challenge/new", views.InstructorCreateNewChallenge, name="instructor-create-new-challenge-url"),

    # ? Instructor Create New Virtual Network
    path("instructor/virtual-network/create/new" , views.InstructorVirturalNetworkNew, name="instructor-virutal-network-create-url"),

    # ? Instructor Courses List
    path("instructor/courses", views.CoursesList, name="courses-all-url"),

    # ? Instructor Students List
    path("instructor/students", views.StudentList, name="students-all-url"),

    # ? Instructor Virutal Networks
    path("instructor/virtaul-networks", views.InstructorVirtualNetworkList, name="instructor-virtual-network-url"),

    # ? Instructor Networks Details
    path("instructor/networks/<int:vn_id>/detail", views.InstructorMachineDetail, name="instructor-machine-detail-url"),

    # ? Instructor Courses Detials
    path("instructor/courses/<int:course_id>/details", views.InstructorCourseDetails, name="instructor-courses-details-url"),

    # ? Instructor Challenge Details
    path("instructor/courses/<int:course_id>/challenge/<int:challenge_id>/", views.InstructorChallengeDetails, name="instructor-challenge-details-url"),

    # ? Instructor Virutal Network
    path("instructor/course/approval/<int:course_id>/", views.InstructorApproveCourse, name="instructor-approve-course-url"),
    
    # ==========================================================
    # ? Student Dashbaord
    path("student/", views.StudentDashboard, name="student-dasboard-url"),
    
    # ? Student Profile
    path("student/profile", views.StudentProfile, name="student-profile-url"),

    # ? Student Courses
    path("student/courses", views.StudentCourses, name="student-courses-url"),

    # ? Student Courses Detials 
    path("student/courses/details/<int:course_id>", views.StudentCourseDetails, name="student-courses-details-url"),

    # ? Student Networks
    path("student/networks", views.StudentMachines, name="student-machines-url"),
    
    # ? Student Networks Details
    path("student/networks/<int:vn_id>/detail", views.StudentMachineDetail, name="student-machine-detail-url"),

    # ? Student Challenge Details
    path("student/courses/<int:course_id>/challenge/<int:challenge_id>/", views.StudentChallengeDetails, name="student-challenge-details-url"),
    
    # ? Student Challenge Flag Submission
    path("student/courses/<int:course_id>/challenge/<int:challenge_id>/<int:submission_id>/flag/submission", views.StudentChallengeFlagSubmission, name="student-challenge-flag-submission-url"),

]

