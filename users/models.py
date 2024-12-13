from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Кастомная модель описания пользователя"""
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    email = models.EmailField(_("email address"), blank=True, null=True)
    mentor = models.ForeignKey(
        "self", on_delete=models.CASCADE,
        related_name='students', null=True, blank=True)

    REQUIRED_FIELDS = ['password']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
