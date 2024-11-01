from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_str, name='main_str'),
    path('create-topic/', views.create_topic, name='create-topic'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('topic/', views.topic, name='topic'),
]