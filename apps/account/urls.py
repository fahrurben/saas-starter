from django.urls import path

from .views import CustomLoginView, RegisterView, VerifiyUserView

urlpatterns = [
    path("login", CustomLoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path("verify-user", VerifiyUserView.as_view(), name="verify-user"),
]
