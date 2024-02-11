from django.urls import path
from .views.user_registration_view import UserRegistrationView
from .views.user_login_view import UserLoginView
from .views.user_view import UserProfileView, UserLogoutView, ChangePasswordView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]