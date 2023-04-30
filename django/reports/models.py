import os
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from software.models import Software
from environments.models import Environment
from django.contrib.auth.models import User

class Report(models.Model):
    owner          = models.ForeignKey(User, on_delete=models.CASCADE)
    title          = models.CharField(max_length=256, blank=False, verbose_name="Название")
    cwe            = models.IntegerField(blank=False, verbose_name="Номер CWE")
    description    = models.TextField(blank=False, verbose_name="Описание")
    software       = models.ForeignKey(Software, on_delete=models.PROTECT, unique=False, blank=False, verbose_name="ПО")
    environments   = models.ManyToManyField(Environment, verbose_name="Среды исполнения")
    exploitability = models.PositiveSmallIntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name="Эксплуатабельность")
    danger         = models.PositiveSmallIntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name="Опасность")
    exploitation   = models.TextField(blank=False, default='Нет', verbose_name="Способ эксплуатации")
    created        = models.DateTimeField(auto_now_add=True)
    updated        = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('report', kwargs={'report_id': self.pk})

class InputFiles(models.Model):
    report    = models.ForeignKey(Report, on_delete=models.CASCADE, unique=False)
    upload    = models.FileField(upload_to='uploads/%Y/%m/%d/', verbose_name="Файлы входных данных")

class DumpFiles(models.Model):
    report    = models.ForeignKey(Report, on_delete=models.CASCADE, unique=False)
    upload    = models.FileField(upload_to='uploads/%Y/%m/%d/', verbose_name="Файлы дампа памяти")