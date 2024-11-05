from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_str, name='main_str'),
    path('category/<str:category>/', views.main_str, name='category_filter'),
    path('create-topic/', views.create_topic, name='create-topic'),
    path('signup/', views.register, name='signup'),
    path('verify_email/<str:token>/', views.verify_email, name='verify_email'),
    path('signin/', views.user_login, name='signin'),
    path('topic/<int:id>/', views.single_topic, name='single_topic'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
