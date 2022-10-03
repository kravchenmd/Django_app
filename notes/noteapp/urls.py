from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/', views.tag, name='user_tag'),
    path('note/', views.note, name='note'),
    path('detail/<int:note_id>', views.detail, name='detail'),
]
