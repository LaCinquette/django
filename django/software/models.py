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

    owner         = models.ForeignKey(User, on_delete=models.CASCADE)
    category      = models.CharField(max_length=1, blank=False, choices=Categories.choices, default='A')
    title         = models.CharField(max_length=100, blank=False)
    version       = models.CharField(max_length=100, blank=False, default='Unknown')
    build_options = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('software', kwargs={'software_id': self.pk})
    
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['category', 'title', 'version', 'build_options'], name='unique_row_software')
    #     ]