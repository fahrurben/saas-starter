from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.account.models import CustomUser, GenderType, UserProfile
from apps.company.models import Company
from django.utils.text import slugify


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    subdomain = serializers.CharField(required=False)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        subdomain = data.get("subdomain")

        if email and password:
            # Authenticate the user against Django's authentication backends
            user = authenticate(email=email, password=password)

            profile = UserProfile.objects.filter(user=user).first()
            if profile is None:
                raise serializers.ValidationError("Invalid email or password.")

            company = profile.company

            if subdomain:
                company = Company.objects.filter(subdomain=subdomain).first()

            if not user:
                raise serializers.ValidationError("Invalid email or password.")

            if not user.is_active:
                raise serializers.ValidationError("This user account is disabled.")

            if not company:
                raise serializers.ValidationError("This user company is not exist")
        else:
            raise serializers.ValidationError("Must include both email and password.")

        # Pass the validated user object down to the view
        data["user"] = user
        data["subdomain"] = company.subdomain
        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        subdomain = self.context["request"].data.get("subdomain")

        self.refresh.access["subdomain"] = subdomain
        self.refresh["subdomain"] = subdomain

        return data


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, max_length=100)
    first_name = serializers.CharField(required=True, max_length=100)
    last_name = serializers.CharField(required=True, max_length=100)
    company_name = serializers.CharField(required=True, max_length=255)
    birthday = serializers.DateField(required=True)
    gender = serializers.ChoiceField(required=True, choices=GenderType.choices)

    def validate_email(self, value):
        is_exist = CustomUser.objects.filter(email=value).first()

        if is_exist:
            raise serializers.ValidationError("Email already exist")

        return value

    def validate_company_name(self, value):
        slug = slugify(value)

        is_exist = Company.objects.filter(subdomain=slug).first()

        if is_exist:
            raise serializers.ValidationError("Company name already exist")

        return value
