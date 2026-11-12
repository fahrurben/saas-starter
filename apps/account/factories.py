import factory
import datetime

from .models import Company, CustomUser, UserProfile, GenderType


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Sequence(lambda n: "Company {}".format(n))


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        django_get_or_create = ("username", "email")

    email = factory.Sequence(lambda n: f"user_{n}@test.com")
    username = factory.LazyAttribute(lambda o: o.email)
    password = "secret123"
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_verified = True
    verification_code = "123456"

    # Properly hash the password after the user instance is initialized
    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password_to_set = extracted
        if password_to_set:
            self.set_password(password_to_set)
            if create:
                self.save()


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(CustomUserFactory)
    company = factory.SubFactory(CompanyFactory)
    birthday = datetime.date(1990, 1, 1)
    gender = GenderType.MALE
