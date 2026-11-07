from django.contrib.auth.models import AbstractUser
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
            is_active=is_active,
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_verified=True,
        )

        user.set_password(password)

        user.save(using=self.db)

        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            is_superuser=True,
            is_staff=True,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractUser):

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_verified = models.BooleanField()
    verification_code = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(db_index=True, auto_now=True)

    objects = BaseUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

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
    gender = models.CharField(
        max_length=1, choices=GenderType.choices, default=GenderType.MALE
    )
    birthday = models.DateField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
