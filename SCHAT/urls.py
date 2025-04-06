from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import upload_status




urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.student_login, name='login'),
    path('san/', views.san, name='san' ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/<int:student_id>/', views.edit_profile, name='edit_profile'),
    path('success/', views.success_view, name='success'),
    path('edit_message/<int:message_id>/', views.edit_message, name='edit_message'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('change-password/', views.change_password, name='change_password'),
    path('chat_board/', views.chat_board, name='chat_board'),
    path('edit_message/<int:message_id>/', views.edit_message, name='edit_message'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('upload-status/', upload_status, name='upload_status'),
    path('all-statuses/', views.all_statuses, name='all_statuses'),
    path('delete-status/<int:status_id>/', views.delete_status, name='delete_status'),
    path('video_call/<str:room_name>/', views.video_call, name='video_call'),

    path('search_page', views.search_page, name='search_page'),
    path('search/', views.get_search_result, name='get_search_result'),

]