# Generated by Django 5.1.2 on 2024-11-04 02:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_tag_remove_topic_tags_topic_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=50, verbose_name='Автор комментария')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('image', models.ImageField(blank=True, null=True, upload_to='comment_images/', verbose_name='Изображение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='forum.topic')),
            ],
        ),
    ]
