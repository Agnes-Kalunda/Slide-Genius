from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('chat/', views.chat_view, name='chat'),
    path('create_presentation/', views.create_presentation, name='create_presentation')
]