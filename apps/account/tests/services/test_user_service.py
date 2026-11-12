import datetime

import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from apps.account.factories import CompanyFactory, CustomUserFactory
from apps.account.models import CustomUser, GenderType
from apps.account.services import register_company, verify_user


@pytest.mark.django_db
def test_register_company(faker):
    register_company(
        email=faker.email(),
        password="secret123",
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        company_name=faker.name(),
        birthday=datetime.date(1990, 1, 1),
        gender=GenderType.MALE,
    )

    assert CustomUser.objects.count() == 1


@pytest.mark.django_db
def test_register_existing_company(faker):
    existing_company = CompanyFactory()
    with pytest.raises(Exception) as context:
        register_company(
            email=faker.email(),
            password=faker.password(),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            company_name=existing_company.name,
            birthday=datetime.date(1990, 1, 1),
            gender=GenderType.MALE,
        )

    assert isinstance(context.value, IntegrityError)


@pytest.mark.django_db
def test_register_existing_email(faker):
    existing_user = CustomUserFactory()

    with pytest.raises(Exception) as context:
        register_company(
            email=existing_user.email,
            password=faker.password(),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            company_name=faker.name(),
            birthday=datetime.date(1990, 1, 1),
            gender=GenderType.MALE,
        )

    assert isinstance(context.value, ValidationError)


@pytest.mark.django_db
def test_verify_user(faker):
    user = CustomUserFactory()
    verification_code = user.verification_code

    is_verified = verify_user(user=user, verification_code=verification_code)

    assert is_verified == True
    assert user.is_verified == True
