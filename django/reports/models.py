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
    title          = models.CharField(max_length=256, blank=False)
    cwe            = models.IntegerField(blank=False)
    description    = models.TextField(blank=False)
    software       = models.ForeignKey(Software, on_delete=models.PROTECT, unique=False, blank=False)
    environments   = models.ManyToManyField(Environment)
    exploitability = models.PositiveSmallIntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(10)])
    danger         = models.PositiveSmallIntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(10)])
    exploitation   = models.TextField(blank=False, default='Нет')
    created        = models.DateTimeField(auto_now_add=True)
    updated        = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('report', kwargs={'report_id': self.pk})

class InputFiles(models.Model):
    report    = models.ForeignKey(Report, on_delete=models.CASCADE, unique=False)
    upload    = models.FileField(upload_to='uploads/%Y/%m/%d/')

class DumpFiles(models.Model):
    report    = models.ForeignKey(Report, on_delete=models.CASCADE, unique=False)
    upload    = models.FileField(upload_to='uploads/%Y/%m/%d/')