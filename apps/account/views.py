from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.account.constant import SUCCESS_RESPONSE
from apps.account.services import register_company

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
