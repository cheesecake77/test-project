from typing import Final, final

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.contrib.auth import get_user_model
#: That's how constants should be defined.
_POST_TITLE_MAX_LENGTH: Final = 80


@final
class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password):
        user = self.model(email=email)
        user.set_password = password
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


@final
class UserProfile(AbstractUser):
    profile_image = models.FileField(upload_to='profile_image', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Custom User"

    def __str__(self):
        return self.email


@final
class PasswordCategory(models.Model):
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category_name = models.CharField("Category Name", max_length=200)

    class Meta:
        verbose_name_plural = "Password Categories"

    def __str__(self):
        return f'{self.created_by.username} - {self.category_name}'


@final
class Password(models.Model):
    comment = models.CharField("Info about password", max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    categoryName = models.ForeignKey(PasswordCategory, on_delete=models.SET_NULL)
    uri = models.CharField("URI", max_length=256, blank=True, null=True)
    encryptedPassword = models.CharField("Encrypted Password", max_length=256, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Passwords"

    def __str__(self):
        return f'Password created by {self.created_by.username}'
