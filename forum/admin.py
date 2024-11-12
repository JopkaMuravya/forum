from django.contrib import admin
from .models import CustomUser, Topic, Comment

admin.site.register(CustomUser)
admin.site.register(Topic)
admin.site.register(Comment)

