from typing import ClassVar

from django.db import models

from apps.common.models import BaseModel


class Company(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    subdomain = models.SlugField(max_length=150, unique=True)

    objects: ClassVar[models.Manager["Company"]] = models.Manager()
