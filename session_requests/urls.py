from django.urls import path
from . import views

urlpatterns = [
    path('request/<int:mentor_id>/', views.request_session, name='request_session'),
    path('list/', views.session_list, name='session_list'),
    path('respond/<int:session_id>/<str:action>/', views.respond_to_session, name='respond_to_session'),
    path('learning-dashboard/', views.dashboard, name='dashboard'),
]
