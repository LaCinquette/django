# Generated by Django 4.2 on 2023-05-02 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('software', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='software',
            name='build_options',
            field=models.TextField(blank=True, verbose_name='Опции сборки'),
        ),
        migrations.AlterField(
            model_name='software',
            name='category',
            field=models.CharField(choices=[('G', 'Графическое'), ('C', 'Консольное'), ('L', 'Библиотека'), ('A', 'Приложение')], default='A', max_length=1, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='software',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='software',
            name='version',
            field=models.CharField(default='Unknown', max_length=100, verbose_name='Версия'),
        ),
    ]
