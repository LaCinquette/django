from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Environment(models.Model):
    class OS(models.TextChoices):
        LINUX   = 'L', _('Linux')
        BSD     = 'B', _('BSD')
        MAC     = 'M', _('Mac')
        WINDOWS = 'W', _('Windows')
        ANDROID = 'A', _('Android')
        IOS     = 'I', _('IOS')
        ANY     = 'N', _('Any OS')
        OTHER   = 'O', _('Other')

    owner   = models.ForeignKey(User, on_delete=models.CASCADE)
    os      = models.CharField(max_length=1, choices=OS.choices, blank=False, default='O')
    version = models.CharField(max_length=256, blank=True)

    def get_absolute_url(self):
        return reverse('environment', kwargs={'environment_id': self.pk})
    
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['os', 'version'], name='unique_row_environment')
    #     ]