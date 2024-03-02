from django.urls import path
from . import views

urlpatterns = [
    path('', views.GetRoutesView.as_view()),
    path('rooms/', views.GetRoomsView.as_view()),
    path('room/<int:room_id>/', views.GetRoomView.as_view()),
]

