# Generated by Django 5.1.2 on 2024-11-05 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_topic_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='likes',
        ),
    ]
