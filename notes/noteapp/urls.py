from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/', views.tag, name='user_tag'),
]
