from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_str, name='main_str'),
    path('category/<str:category>/', views.main_str, name='category_filter'),
    path('create-topic/', views.create_topic, name='create-topic'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('topic/', views.topic, name='topic'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)