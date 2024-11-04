from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_str, name='main_str'),
    path('create-topic/', views.create_topic, name='create-topic'),
    path('signup/', views.register, name='signup'),
    path('signin/', views.user_login, name='signin'),
    path('topic/', views.topic, name='topic'),
]