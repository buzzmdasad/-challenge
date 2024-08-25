from django.urls import path
from .views import (
    RecruiterSignupView, SeekerSignupView, LoginView,
    RecruiterProfileView, SeekerProfileView, LogoutView,CreateTokenView,ManageUserView,
)

urlpatterns = [
    path('recruiter/signup/', RecruiterSignupView.as_view(), name='recruiter-signup'),
    path('seeker/signup/', SeekerSignupView.as_view(), name='seeker-signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('recruiterprofile/', RecruiterProfileView.as_view(), name='recruiterprofile'),
    path('seekerprofile/', SeekerProfileView.as_view(), name='seekerprofile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', CreateTokenView.as_view(), name='token'),
]
