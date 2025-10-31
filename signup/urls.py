from django.urls import path
from . import views

app_name = "signup"

urlpatterns = [
    path("", views.coming_soon, name="coming_soon"),
    path("subscribe/", views.subscribe_email, name="subscribe_email"),
    path("verify/", views.verify_code, name="verify_code"),
    path("resend/", views.resend_code, name="resend_code"),
]
