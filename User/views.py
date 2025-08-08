from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from .serializers import OTPSendSerializer, CheckOTPSerializer, UserCreateSerializer
from .models import OTP, UserModel
from .utils import generate_otp

DEBUG = settings.DEBUG


class RequestOTPView(APIView):
    @swagger_auto_schema(
        operation_summary="Request OTP for phone number verification",
        request_body=OTPSendSerializer,
        responses={
            200: openapi.Response(description="OTP sent successfully."),
            400: openapi.Response(
                description="Phone number already registered or invalid input."
            ),
        },
        tags=["Authentication"],
    )
    def post(self, request, *args, **kwargs):
        serializer = OTPSendSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        phone_number = serializer.validated_data["phone_number"]

        try:
            user = UserModel.objects.get(phone_number=phone_number)
            if user:
                return Response(
                    {"message": "Phone Number already registrated"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except UserModel.DoesNotExist:
            if not DEBUG:
                otp = str(generate_otp())
                pass
            else:
                otp = "123456"

            OTP.objects.create(phone_number=phone_number, otp_code=otp)

            return Response(
                {"message": "OTP sent successfully."}, status=status.HTTP_200_OK
            )


class CheckOTPView(APIView):
    @swagger_auto_schema(
        operation_summary="Verify OTP",
        request_body=CheckOTPSerializer,
        responses={
            200: openapi.Response(description="User verified succesfullhy."),
            400: openapi.Response(
                description="Phone number already registered or invalid input."
            ),
        },
        tags=["Authentication"],
    )
    def post(self, request, *args, **kwargs):
        serializer = CheckOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        phone_number = serializer.validated_data["phone_number"]
        otp_code = serializer.validated_data["otp_code"]

        try:
            user = OTP.objects.get(phone_number=phone_number)
            if user.otp_code != otp_code:
                return Response(
                    {
                        "error": {
                            "phone_number": phone_number,
                            "status": "incorrect code",
                        }
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.is_verified = True
            user.save()
            return Response(
                {"message": {"phone_number": phone_number, "status": "verified"}},
                status=status.HTTP_200_OK,
            )
        except OTP.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class UserCreateView(APIView):
    @swagger_auto_schema(
        operation_summary="User Create",
        request_body=UserCreateSerializer,
        responses={
            200: openapi.Response(description="User verified succesfullhy."),
            400: openapi.Response(
                description="Phone number already registered or invalid input."
            ),
        },
        tags=["Authentication"],
    )
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        phone_number = serializer.validated_data["phone_number"]

        try:
            otp_user = OTP.objects.get(phone_number=phone_number)
            if not otp_user.is_verified:
                return Response(
                    {"error": "Phone number is not verified"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            otp_user.delete()
            serializer.save()
            return Response(
                {"message": "Created Successfully", "data": serializer.data}
            )
        except OTP.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
