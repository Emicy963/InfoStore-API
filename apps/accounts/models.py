from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        CLIENT = 'client', _('Client')

    email = models.EmailField(_('email address'), unique=True)
    avatar_url = models.URLField(blank=True, null=True)
    full_name = models.CharField(_('full name'), max_length=150)
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    # role = models.CharField(
    #     _('role'),
    #     max_length=10,
    #     choices=Role.choices,
    #     default=Role.CLIENT,
    # )
    created_at = models.DateTimeField(_('cretead at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']

    def __str__(self):
        return self.email

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True)
#     birth_date = models.DateField(_('address'), blank=True, null=True)
#     created_at = models.DateTimeField(_('created at'), auto_now_add=True)
#     updated_at = models.DateTimeField(_('updated at'), auto_now=True)

#     class Meta:
#         verbose_name = _('Profile')
#         verbose_name_plural = _('Profiles')

#     def __str__(self):
#         return f'Profile of {self.user.email}'
