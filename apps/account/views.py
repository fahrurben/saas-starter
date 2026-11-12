from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.account.constant import SUCCESS_RESPONSE
from apps.account.models import CustomUser
from apps.account.services import register_company, verify_user

from .serializers import CustomLoginSerializer, RegisterSerializer


class CustomLoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            subdomain = serializer.validated_data["subdomain"]

            # Fetch existing token or create a new one for the user
            refresh = RefreshToken.for_user(user)
            refresh["subdomain"] = subdomain

            # Return custom payload back to the client
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            register_company(
                email=validated_data.get("email"),
                password=validated_data.get("password"),
                first_name=validated_data.get("first_name"),
                last_name=validated_data.get("last_name"),
                company_name=validated_data.get("company_name"),
                birthday=validated_data.get("birthday"),
                gender=validated_data.get("gender"),
            )

            return Response(SUCCESS_RESPONSE)


class VerifiyUserView(TemplateView):

    def get(self, request):
        verification_code = request.GET.get("verification_code")

        user = CustomUser.objects.filter(
            is_verified=False, verification_code=verification_code
        ).first()

        verification_status = False

        if user:
            verification_status = verify_user(
                user=user, verification_code=verification_code
            )

        context = {
            "user": user,
            "verification_status": verification_status,
        }

        return render(request, "verify_user.html", context)
