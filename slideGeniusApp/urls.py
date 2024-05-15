from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('next/', next_slide, name='next_slide'),
    path('previous/', previous_slide, name='previous_slide'),
]
