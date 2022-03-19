import textwrap
from typing import Final, final

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

#: That's how constants should be defined.
_POST_TITLE_MAX_LENGTH: Final = 80


@final
class BlogPost(models.Model):
    """
    This model is used just as an example.
    With it, we show how one can:
    - Use fixtures and factories
    - Use migrations testing
    """

    title = models.CharField(max_length=_POST_TITLE_MAX_LENGTH)
    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        verbose_name = 'BlogPost'  # You can probably use `gettext` for this
        verbose_name_plural = 'BlogPosts'

    def __str__(self) -> str:
        """All django models should have this method."""
        return textwrap.wrap(self.title, _POST_TITLE_MAX_LENGTH // 4)[0]


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
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email", unique=True, max_length=255, blank=True, null=True)
    username = models.CharField("User Name", unique=True, max_length=255, blank=True, null=True)
    profile_image = models.FileField(upload_to='profile_image', blank=True, null=True)
    user_secret_key = models.CharField('User Secret Key', max_length=500, blank=True, null=True)
    is_active = models.BooleanField('Active', default=True)
    is_staff = models.BooleanField('Staff', default=False)
    is_superuser = models.BooleanField('Super User', default=False)
    objects = CustomUserManager()
    USERNAME_FILED = 'email'

    class Meta:
        verbose_name_plural = "Custom User"

    def __str__(self):
        return self.email


@final
class PasswordCategory(models.Model):
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category_name = models.CharField("Category Name", max_length=200)

    class Meta:
        verbose_name_plural = "Password Categories"

    def __str__(self):
        return str(self.created_by.username) + '-' + str(self.category_name)


@final
class Password(models.Model):
    comment = models.CharField("Info about password", max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    categoryName = models.ForeignKey(PasswordCategory, on_delete=models.CASCADE)
    uri = models.CharField("URI", max_length=256, blank=True, null=True)
    encryptedPassword = models.CharField("Encrypted Password", max_length=256, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Passwords"

    def __str__(self):
        return "Password created by " + str(self.created_by.username)
