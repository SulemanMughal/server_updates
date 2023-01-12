from django.urls import path

from .views import CourseAPIView

urlpatterns = [ 
    path('', CourseAPIView.as_view()), 
]