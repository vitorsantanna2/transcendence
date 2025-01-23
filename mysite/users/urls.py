from django.urls import path
from .views import LoginView, TwoFactorAuthView, RegisterView

urlpatterns = [
    # Registration endpoint
    path("register/", RegisterView.as_view(), name="register"),
    # Login and 2FA endpoints
    path("login/", LoginView.as_view(), name="login"),
    path(
        "twofa/", TwoFactorAuthView.as_view(), name="twofa"
    ),  # Updated to use TwoFactorAuthView
]
