from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class Profile(models.Model):
    # class Occupations(models.TextChoices):
    #     JUNIOR   = 'J', _('Графическое')
    #     MIDDLE     = 'C', _('Консольное')
    #     SENIOR     = 'L', _('Библиотека')
    #     APPLICATION = 'A', _('Приложение')

    user         = models.OneToOneField(User, on_delete=models.CASCADE)
    patronymic   = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
    born         = models.DateField(blank=False, verbose_name='Дата рождения')
    phone_regex  = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False, unique=True, verbose_name='Номер телефона') # Validators should be a list