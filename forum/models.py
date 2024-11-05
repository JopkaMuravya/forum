from django.db import models
import random
from django.contrib.auth.models import User

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор темы")

    def __str__(self):
        return self.title

class Comment(models.Model):
    topic = models.ForeignKey(Topic, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    text = models.TextField(verbose_name="Текст комментария")
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Комментарий от {self.author.username} к теме {self.topic}"