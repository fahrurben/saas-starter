from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

import rest_framework_simplejwt
from apps.account.constant import SUCCESS_RESPONSE
from apps.account.models import CustomUser
from apps.account.services import invite_user, register_company, verify_user

from apps.common.mixins import (
    CustomListModelMixin,
    CustomRetrieveModelMixin,
    CustomDestroyModelMixin,
)
from apps.company.models import Company

from .serializers import (
    CustomLoginSerializer,
    InviteSerializer,
    RegisterSerializer,
    UserSerializer,
)


class CustomLoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            company_id = serializer.validated_data["company_id"]

            # Fetch existing token or create a new one for the user
            refresh = RefreshToken.for_user(user)
            refresh["company_id"] = company_id

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


class UserConfirmationView(TemplateView):
    pass


class ManageUserView(
    CustomListModelMixin,
    CustomRetrieveModelMixin,
    CustomDestroyModelMixin,
    GenericViewSet,
):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [rest_framework_simplejwt.authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company_id = self.request.auth.get("company_id")
        return CustomUser.objects.filter(userprofile__company_id=company_id)

    @action(detail=False, methods=["post"])
    def invite(self, request):
        company_id = self.request.auth.get("company_id")
        serializer = InviteSerializer(
            data=request.data, context={"company_id": company_id}
        )
        company = Company.objects.get(id=company_id)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data

            invite_user(
                email=validated_data.get("email"),
                first_name=validated_data.get("first_name"),
                last_name=validated_data.get("first_name"),
                company=company,
                birthday=validated_data.get("birthday"),
                gender=validated_data.get("gender"),
            )

            return Response(SUCCESS_RESPONSE)
