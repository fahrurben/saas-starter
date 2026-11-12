import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import slugify

from apps.account.models import CustomUser, GenderType, UserProfile
from apps.company.models import Company


def send_templated_email(recipient_email, context_data):
    """
    Renders an HTML template and sends it as a multipart email.
    """
    subject = "Welcome to Our Platform!"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [recipient_email]

    html_content = render_to_string("emails/welcome_email.html", context_data)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")

    msg.send()


@transaction.atomic
def register_company(
    *,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    company_name: str,
    birthday: datetime.date,
    gender: GenderType
):
    user = CustomUser.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        is_verified=False,
        is_active=True,
    )

    subdomain = slugify(company_name)
    company = Company.objects.create(name=company_name, subdomain=subdomain)

    UserProfile.objects.create(
        user=user,
        company=company,
        gender=gender,
        birthday=birthday,
    )

    verify_user_url = reverse(
        "apps:accounts:verify-user", query={"verification_code": user.verification_code}
    )
    send_templated_email(
        user.email, {"first_name": user.first_name, "verify_user_url": verify_user_url}
    )

    return user


@transaction.atomic
def verify_user(*, user: CustomUser, verification_code: str) -> bool:
    if user.verification_code == verification_code:
        user.is_verified = True
        user.save(update_fields=["is_verified"])
        return True

    return False


@transaction.atomic
def invite_user(
    *,
    email: str,
    first_name: str,
    last_name: str,
    company: Company,
    birthday: datetime.date,
    gender: GenderType
):
    is_user_exists = CustomUser.objects.filter(email=email).exists()

    if is_user_exists:
        raise Exception("User with same email already exists")

    user = CustomUser.objects.create_user(
        email=email,
        password=None,
        first_name=first_name,
        last_name=last_name,
        is_verified=False,
        is_active=True,
    )

    user_profile = UserProfile.objects.create(
        user=user,
        company=company,
        gender=gender,
        birthday=birthday,
    )

    return user_profile
