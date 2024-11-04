# Generated by Django 5.1.2 on 2024-11-03 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_topic_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Тег')),
                ('color', models.CharField(default='#000000', max_length=7, verbose_name='Цвет')),
            ],
        ),
        migrations.RemoveField(
            model_name='topic',
            name='tags',
        ),
        migrations.AddField(
            model_name='topic',
            name='tags',
            field=models.ManyToManyField(blank=True, to='forum.tag', verbose_name='Теги'),
        ),
    ]
