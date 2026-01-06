from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_list, name='chat_list'),
    path('chat/<int:user_id>/', views.chat_detail, name='chat_detail'),
    path('request/session/<int:skill_id>/', views.request_session, name='request_session'),
    path('requests/', views.request_list, name='request_list'),
    path('requests/<int:request_id>/<str:action>/', views.respond_request, name='respond_request'),
]
