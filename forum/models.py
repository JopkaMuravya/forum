from django.db import models

class Topic(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок темы")
    category = models.CharField(max_length=100, verbose_name="Категория")
    description = models.TextField(verbose_name="Описание")
    tags = models.CharField(max_length=200, verbose_name="Теги")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    image = models.ImageField(upload_to='topic_images/', blank=True, null=True, verbose_name="Изображение")

    def __str__(self):
        return self.title