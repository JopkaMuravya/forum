from django.db import models
import random
from django.contrib.auth.models import User, AbstractUser
from mysite import settings
import markdown
import bleach

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Тег")
    color = models.CharField(max_length=7, verbose_name="Цвет", default="#000000")

    def save(self, *args, **kwargs):
        if not self.color or self.color == "#000000":
            self.color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Topic(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок темы")
    category = models.CharField(max_length=100, verbose_name="Категория")
    description = models.TextField(verbose_name="Описание")
    tags = models.ManyToManyField(Tag, verbose_name="Теги", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    image = models.ImageField(upload_to='topic_images/', blank=True, null=True, verbose_name="Изображение")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор темы")
    avatar = models.ImageField(upload_to='avatar_images/', blank=True, null=True, verbose_name="Аватар темы")

    def get_markdown(self):
        html = markdown.markdown(self.description, extensions=['fenced_code'])
        allowed_tags = list(bleach.sanitizer.ALLOWED_TAGS) + ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre']
        print(allowed_tags)
        return bleach.clean(html, tags=allowed_tags)


    def __str__(self):
        return self.title


class Comment(models.Model):
    topic = models.ForeignKey(Topic, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор комментария")
    avatar = models.ImageField(upload_to='avatar_images/', blank=True, null=True, verbose_name="Аватар комментария")
    text = models.TextField(verbose_name="Текст комментария")
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def get_markdown(self):
        html = markdown.markdown(self.text, extensions=['fenced_code'])
        allowed_tags = list(bleach.sanitizer.ALLOWED_TAGS) + ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre']
        print(allowed_tags)
        return bleach.clean(html, tags=allowed_tags)


    def __str__(self):
        return f"Комментарий от {self.author.username} к теме {self.topic}"


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatar_images/', blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, blank=True, null=True)


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'topic')


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=10, choices=[('like', 'Like'), ('reply', 'Reply')])
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.notification_type} on {self.topic.title}"

