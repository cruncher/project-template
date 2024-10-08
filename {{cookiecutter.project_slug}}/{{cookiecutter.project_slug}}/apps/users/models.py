import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):

        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email))
        if password:
            user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):

        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4)
    username = models.CharField(max_length=512, blank=True, null=True, editable=False)
    email = models.EmailField(verbose_name="email address", max_length=512, unique=True)
    mobile_phone = models.CharField(max_length=50, blank=True, null=True)

    mobile_phone_validated = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_full_name() or self.email
