from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager as BUM
from django.db import models

from apps.common.models import BaseModel
from apps.company.models import Company


class BaseUserManager(BUM):

    def create_user(
        self,
        email,
        password,
        first_name,
        last_name,
        is_verififed,
        is_active=True,
        is_superuser=False,
        is_staff=False,
    ):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have password")

        user = self.model(
            email=self.normalize_email(email.lower()),
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_verified=is_verififed,
        )

        user.setPassword(password)

        user.full_clearn()
        user.save(using=self.db)

        return user

    def create_super_user(self, email, password, first_name, last_name):
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_verififed=True,
            is_active=True,
            is_superuser=True,
            is_staff=True,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class CustomUser(BaseModel, AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_verified = models.BooleanField()
    verification_code = models.CharField(max_length=10, null=True)

    USERNAME_FIELD = "email"

    class Meta:
        permissions = [
            ("invite_user", "Can invite user"),
        ]

    def __str__(self):
        return str(self.email)


class GenderType(models.TextChoices):
    MALE = "M", "Male"
    FEMAIL = "F", "Female"


class UserProfile(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    company = models.ForeignKey(Company, on_delete=models.RESTRICT)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=1, choices=GenderType.choices, default=GenderType.MALE
    )
    birthday = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
