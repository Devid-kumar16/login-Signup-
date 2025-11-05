from django.urls import path, include
from .views import authView, home, RegisterView, loginView, logoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("", home, name="home"),
    path("signup/", authView, name="authView"),
    # custom login view (overrides the auth urls login)
    path("accounts/login/", loginView, name="login"),
    path("accounts/logout/", logoutView, name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/register/", RegisterView.as_view(), name="register"),
    
    # JWT token endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
