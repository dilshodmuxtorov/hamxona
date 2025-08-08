from django.urls import path

from .views import RequestOTPView, CheckOTPView, UserCreateView

urlpatterns = [
    path("request-otp/",RequestOTPView.as_view()),
    path('check-otp/', CheckOTPView.as_view()),
    path('user-create/', UserCreateView.as_view())
]