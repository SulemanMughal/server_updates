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


    # ==========================================================
    # ? Instructor Dashbaord
    path("instructor/", views.InstructorDashboard, name="instructor-dasboard-url"),


    # ==========================================================
    # ? Student Dashbaord
    path("student/", views.StudentDashboard, name="student-dasboard-url"),
    
    # ? Student Profile
    path("student/profile", views.StudentProfile, name="student-profile-url"),

]

