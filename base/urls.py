from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_page, name='logout'),

    path('', views.home_page, name='home'),
    path('profile/<int:user_id>', views.profile_page, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    path('topics/', views.topics_page, name='topics'),
    path('recent_activities/', views.activity_page, name='activity'),

    path('room/<int:room_id>/', views.room_page, name='room'),
    path('create_room/', views.create_room, name='create_room'),
    path('update_room/<int:room_id>/', views.update_room, name='update_room'),
    path('delete_room/<int:room_id>/', views.delete_room, name='delete_room'),
    path('delete_message/<int:msg_id>/', views.delete_message, name='delete_message'),
]

