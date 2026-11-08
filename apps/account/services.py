import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from django.db import transaction
from apps.account.models import CustomUser, GenderType, UserProfile
from apps.company.models import Company


def send_templated_email(recipient_email, context_data):
    """
    Renders an HTML template and sends it as a multipart email.
    """
    subject = "Welcome to Our Platform!"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [recipient_email]

    # 1. Render the HTML content with the context dictionary
    html_content = render_to_string("emails/welcome_email.html", context_data)

    # 2. Create a clean plain-text version fallback for older clients
    text_content = strip_tags(html_content)

    # 3. Initialize the core multipart email
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)

    # 4. Attach the HTML alternative
    msg.attach_alternative(html_content, "text/html")

    # 5. Send the email
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

    company = Company.objects.create(name=company_name)

    UserProfile.objects.create(
        user=user,
        company=company,
        gender=gender,
        birthday=birthday,
    )

    send_templated_email(
        user.email, {"first_name": user.first_name, "code": user.verification_code}
    )

    return user
