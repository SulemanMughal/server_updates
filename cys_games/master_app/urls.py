from django.urls import path

from . import views


urlpatterns = [
    # ? Home Route
    path('', views.index, name="master_index"),

    # ? User Login Route
    path('login/', views.UserLoginView, name="user-login"),

    # ? User login (Ajax)
    path('login-ajax/', views.UserLoginAjaxView, name="user-login-ajax"),

    # ? User Logout Route
    path('logout/', views.UserLogoutView, name="user-logout"),

    # ? How to Connect VPN
    path("how-to-connect-vpn/", views.ConnectVPN, name="how-to-connect-vpn"),

    # ? Password change
    path('change_password/', views.change_password, name="change_password"),

    # ?  Fetch open stack images
    path("network/images/api", views.FetchNetworkImages,
         name="fetch-network-images-url"),

    # ==========================================================
    # ? Admin Dashbaord
    path("admin/", views.AdminDashboard, name="admin-dasboard-url"),

    # ?  Admin : Recent Activity Monitoring
    path("admin/activity-logs", views.AdminActivityLogs,
         name="admin-activity-logs-url"),

    # ? Admin Profile
    path("admin/profile", views.AdminProfile, name="admin-profile-url"),

    # ? Admin Course List
    path("admin/course", views.AdminCourseList, name="admin-course-list-url"),

    # ? Admin Create New Course
    path("admin/course/new", views.AdminCreateCourse,
         name="admin-course-new-url"),

    # ? Admin Course Details
    path("admin/course/<int:course_id>/details",
         views.AdminCourseDetails, name="admin-courses-details-url"),

    # ? Admin Course Approve
    path("admin/course/<int:vn_id>/approval",
         views.AdminCourseApproval, name="admin-course-approval-url"),

    # ? Admin Course Reject
    path("admin/course/<int:course_id>/reject",
         views.AdminCourseReject, name="admin-course-reject-url"),

    # ? Admin Virutal Networks
    path("admin/virtaul-networks", views.AdminVirtualNetworkList,
         name="admin-virtual-network-url"),

    # ? Admin Craete New Virutal Networks
    path("admin/virtaul-networks/create", views.AdminVirtualNetworkCreate,
         name="admin-virtual-network-create-url"),

    # ? Admin Virutal Networks Details
    path("admin/virtaul-networks/<int:vn_id>/detail",
         views.AdminVirtualNetworkDetails, name="admin-machine-detail-url"),

    # ? Admin Create New Student
    path("admin/students/create", views.AdminStudentCreate,
         name="admin-student-new-url"),

    # ? Admin Students List
    path("admin/students/", views.AdminStudentList,
         name="admin-student-list-url"),

    # ? Admin Instructor List
    path("admin/instructors/", views.AdminInstructorsList,
         name="admin-instructors-list-url"),

    # ? Admin Create New Instructor
    path("admin/instructor/create", views.AdminInstructorCreate,
         name="admin-instructor-new-url"),

    # ? Admin Add a new challenge to an existing course
    path("admin/course/challenge/new", views.AdminChallengeCreate,
         name="admin-challenge-new-url"),

    # ? Admin : Add a new student to an existing course
    path("admin/course/student/new", views.AdminCourseStudentCreate,
         name="admin-course-student-add-url"),



    # TODO  :  # ? Start an instance in openstack (Active Directory Scenario)
    # path("admin/network/<int:vn_id>/instance/active",
    #      views.AdminStartNetworkInstance, name="admin-create-network-instance-url"),

    # ? Create an instance in openstack for requested virtual image
    path("admin/network/<int:vn_id>/instance/create",
         views.AdminCreateNetworkInstance, name="admin-create-network-instance-url"),


    # ? Reset Instance
    path("admin/network/<int:vn_id>/instance/reset",
         views.AdminRebootNetworkInstance, name="admin-reboot-network-instance-url"),

    # ==========================================================
    # ? Instructor Dashbaord
    path("instructor/", views.InstructorDashboard,
         name="instructor-dasboard-url"),




    # ? Instructor Profile
    path("instructor/profile", views.InsturctorProfile,
         name="instructor-profile-url"),

    # ? Instructor Courses List
    path("instructor/courses", views.CoursesList, name="courses-all-url"),

    # ? Instructor Create New Course
    path("instructor/course/new", views.CreateCourse, name="course-new-url"),

    # ? Instructor Courses Detials
    path("instructor/courses/<int:course_id>/details",
         views.InstructorCourseDetails, name="instructor-courses-details-url"),

    # ? Instructor Add Exising Student to a course
    path("instructor/course/students/new",
         views.AddNewStudents, name="course-students-new-url"),

    # ? Instructor Create New Challenge
    path("instructor/course/challenge/new", views.InstructorCreateNewChallenge,
         name="instructor-create-new-challenge-url"),

    # ? Instructor Create New Virtual Network
    path("instructor/virtual-network/create/new", views.InstructorVirturalNetworkNew,
         name="instructor-virutal-network-create-url"),

    # ? Instructor Students List
    path("instructor/students", views.StudentList, name="students-all-url"),

    # ? Instructor Create New Student
    path("instructor/students/create", views.InstructorCreateStudent,
         name="instructor-student-create-url"),

    # ? Instructor Virutal Networks
    path("instructor/virtaul-networks", views.InstructorVirtualNetworkList,
         name="instructor-virtual-network-url"),

    # ? Instructor Networks Details
    path("instructor/networks/<int:vn_id>/detail",
         views.InstructorMachineDetail, name="instructor-machine-detail-url"),

    # ? Instructor Challenge Details
    path("instructor/courses/<int:course_id>/challenge/<int:challenge_id>/",
         views.InstructorChallengeDetails, name="instructor-challenge-details-url"),

    # ? Instructor Virutal Network
    path("instructor/course/approval/<int:course_id>/",
         views.InstructorApproveCourse, name="instructor-approve-course-url"),

    # ?  Instructor : Remove Student from a course
    path("instructor/course/student/remove/<int:student_id>",
         views.InstructorRemoveStudent, name="instructor-remove-student"),

    # ==========================================================
    # ? Student Dashbaord
    path("student/", views.StudentDashboard, name="student-dasboard-url"),

    # ? Student Profile
    path("student/profile", views.StudentProfile, name="student-profile-url"),

    # ? Student Courses
    path("student/courses", views.StudentCourses, name="student-courses-url"),

    # ? Student Courses Detials
    path("student/courses/details/<int:course_id>",
         views.StudentCourseDetails, name="student-courses-details-url"),

    # ? Student Networks
    path("student/networks", views.StudentMachines, name="student-machines-url"),

    # ? Student Networks Details
    path("student/networks/<int:vn_id>/detail",
         views.StudentMachineDetail, name="student-machine-detail-url"),

    # ? Student Challenge Details
    path("student/courses/<int:course_id>/challenge/<int:challenge_id>/",
         views.StudentChallengeDetails, name="student-challenge-details-url"),

    # ? Student Challenge Flag Submission
    path("student/courses/<int:course_id>/challenge/<int:challenge_id>/<int:submission_id>/flag/submission",
         views.StudentChallengeFlagSubmission, name="student-challenge-flag-submission-url"),

    # ? Student Create virtual network instance
    path("student/virtual-network/crate/instance",
         views.StudentCreateNetworkInstance, name="student-create-network-instance"),

    # ? Student Flag Submission
    path("student/flag/submission", views.StudentFlagSubmission,
         name="student-flag-submission"),


    path("contact", views.ContactView, name="contact_url"),

    path("about", views.AboutView, name="about_url"),


    # ?  Create VPN File
    path("create-vpn", views.CreateVPN, name="create_vpn_url"),

]
