# core/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path("login/", UserLoginView.as_view(),name='login'),
    path("logout/",UserLogout.as_view(),name='user_logout'),
    path("refresh-token/",UserRefreshtoken.as_view(),name='refresh_token')
]
