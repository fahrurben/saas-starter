import datetime

from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from apps.account.factories import CompanyFactory, CustomUserFactory
from apps.account.models import CustomUser, GenderType

from apps.account.services import register_company
from faker import Faker


class UserServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()

    def test_register_company(self):
        register_company(
            email=self.faker.email(),
            password="secret123",
            first_name=self.faker.first_name(),
            last_name=self.faker.last_name(),
            company_name=self.faker.name(),
            birthday=datetime.date(1990, 1, 1),
            gender=GenderType.MALE,
        )

        self.assertEqual(1, CustomUser.objects.count())

    def test_register_existing_company(self):
        existing_company = CompanyFactory()
        with self.assertRaises(Exception) as context:
            register_company(
                email=self.faker.email(),
                password=self.faker.password(),
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                company_name=existing_company.name,
                birthday=datetime.date(1990, 1, 1),
                gender=GenderType.MALE,
            )

        self.assertIsInstance(context.exception, IntegrityError)

    def test_register_existing_email(self):
        existing_user = CustomUserFactory()

        with self.assertRaises(Exception) as context:
            register_company(
                email=existing_user.email,
                password=self.faker.password(),
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                company_name=self.faker.name(),
                birthday=datetime.date(1990, 1, 1),
                gender=GenderType.MALE,
            )

        self.assertIsInstance(context.exception, ValidationError)
