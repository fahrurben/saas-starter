from django.urls import path
from rest_framework import routers

from .views import (
    CustomLoginView,
    RegisterView,
    UserConfirmationView,
    VerifiyUserView,
    ManageUserView,
)

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"users", ManageUserView)

urlpatterns = [
    path("login", CustomLoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path("verify-user", VerifiyUserView.as_view(), name="verify-user"),
    path("confirm-user", UserConfirmationView.as_view(), name="confirm-user"),
] + router.urls
