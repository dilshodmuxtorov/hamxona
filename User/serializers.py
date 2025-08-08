from rest_framework import serializers


from .models import OTP, UserModel


class OTPSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ["phone_number"]


class CheckOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ["phone_number", "otp_code"]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "name",
            "surname",
            "phone_number",
            "password",
            "passport_number",
            "pinfll",
            "date_of_birth",
        ]
