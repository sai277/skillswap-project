from django.urls import path
from .views import (
    signup_view,
    login_view,
    logout_view,
    profile_view,
    edit_profile_view,
    index,
)

urlpatterns = [
    path('', index, name='index'),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", edit_profile_view, name="edit_profile"),
]
