from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Software(models.Model):
    class Categories(models.TextChoices):
        GRAPHICAL   = 'G', _('Графическое')
        CONSOLE     = 'C', _('Консольное')
        LIBRARY     = 'L', _('Библиотека')
        APPLICATION = 'A', _('Приложение')

    owner         = models.ForeignKey(User, 
                                      on_delete=models.CASCADE)
    
    category      = models.CharField(max_length=1, 
                                     blank=False, 
                                     choices=Categories.choices, 
                                     default='A', 
                                     verbose_name="Категория")
    
    title         = models.CharField(max_length=100, 
                                     blank=False, 
                                     verbose_name="Название")
    
    version       = models.CharField(max_length=100, 
                                     blank=False, 
                                     default='Unknown', 
                                     verbose_name="Версия")
    
    build_options = models.TextField(blank=True, 
                                     verbose_name="Опции сборки")

    def get_absolute_url(self):
        return reverse('software', kwargs={'software_id': self.pk})
    
    def __str__(self):
        name  = self.title + " " + self.version
        
        if self.build_options:
            name = name + " (" + self.build_options + ")"
        
        return name
    
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category', 'title', 'version', 'build_options'], name='unique_row_software')
    #     ]