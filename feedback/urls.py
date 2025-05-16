# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('give/<int:session_id>/', views.feedback_page, name='feedback_page'),
]
