from django.urls import path

from .views import (
    CustomLoginView,
    CustomLogoutView,
    SignUpView,
    StudentSignUpView,
    TeacherSignUpView,
    ProfileView,
)


app_name = 'account_service'  # pylint: disable=invalid-name

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/student/', StudentSignUpView.as_view(), name='student_signup'),
    path('signup/teacher/', TeacherSignUpView.as_view(), name='teacher_signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
