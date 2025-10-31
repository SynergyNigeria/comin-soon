from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from .models import EmailSubscription


def coming_soon(request):
    """Render the coming soon landing page with pre-registered sellers count"""
    from .models import EmailSubscription

    pre_registered_count = EmailSubscription.objects.count()
    return render(request, "main.html", {"pre_registered_count": pre_registered_count})


@require_POST
@csrf_exempt
def subscribe_email(request):
    """Handle email subscription and send verification code"""
    try:
        data = json.loads(request.body)
        email = data.get("email", "").strip().lower()

        if not email:
            return JsonResponse({"success": False, "message": "Email is required"})

        # Check if email already exists
        subscription, created = EmailSubscription.objects.get_or_create(
            email=email, defaults={"is_verified": False}
        )

        if not created and subscription.is_verified:
            return JsonResponse(
                {"success": False, "message": "This email is already verified"}
            )

        # Generate and send verification code
        subscription.generate_verification_code()

        # Send verification email using main template
        subject = "Verify Your Email - COVU Marketplace"
        try:
            html_message = render_to_string(
                "coming_soon.html",
                {
                    "verification_code": subscription.verification_code,
                    "email": email,
                    "is_email": True,  # flag to adjust template for email context
                },
            )
            plain_message = strip_tags(html_message)
            send_mail(
                subject=subject,
                message=plain_message,
                html_message=html_message,
                from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
                recipient_list=[email],
                fail_silently=False,
            )
            return JsonResponse(
                {"success": True, "message": "Verification code sent to your email"}
            )
        except Exception as e:
            return JsonResponse(
                {
                    "success": False,
                    "message": f"Failed to send verification email: {str(e)}",
                    "debug": str(e),
                }
            )

    except json.JSONDecodeError as e:
        return JsonResponse(
            {
                "success": False,
                "message": f"Invalid request format: {str(e)}",
                "debug": str(e),
            }
        )
    except Exception as e:
        import traceback

        return JsonResponse(
            {
                "success": False,
                "message": f"An error occurred: {str(e)}",
                "debug": traceback.format_exc(),
            }
        )


@require_POST
@csrf_exempt
def verify_code(request):
    """Handle verification code submission"""
    try:
        data = json.loads(request.body)
        email = data.get("email", "").strip().lower()
        code = data.get("code", "").strip()

        if not email or not code:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Email and verification code are required",
                }
            )

        try:
            subscription = EmailSubscription.objects.get(email=email)
        except EmailSubscription.DoesNotExist:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Email not found. Please subscribe first.",
                }
            )

        if subscription.is_verified:
            return JsonResponse(
                {"success": False, "message": "This email is already verified"}
            )

        # Check if code is valid
        if subscription.is_code_valid(code):
            subscription.verify_email()
            return JsonResponse(
                {
                    "success": True,
                    "message": "Email verified successfully! Welcome to COVU.",
                }
            )
        else:
            subscription.increment_attempts()
            attempts_left = 5 - subscription.verification_attempts
            if attempts_left > 0:
                return JsonResponse(
                    {
                        "success": False,
                        "message": f"Invalid verification code. {attempts_left} attempts remaining.",
                    }
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Too many failed attempts. Please request a new verification code.",
                    }
                )

    except json.JSONDecodeError as e:
        return JsonResponse(
            {
                "success": False,
                "message": f"Invalid request format: {str(e)}",
                "debug": str(e),
            }
        )
    except Exception as e:
        import traceback

        return JsonResponse(
            {
                "success": False,
                "message": f"An error occurred: {str(e)}",
                "debug": traceback.format_exc(),
            }
        )


@require_POST
@csrf_exempt
def resend_code(request):
    """Resend verification code"""
    try:
        data = json.loads(request.body)
        email = data.get("email", "").strip().lower()

        if not email:
            return JsonResponse({"success": False, "message": "Email is required"})

        try:
            subscription = EmailSubscription.objects.get(email=email)
        except EmailSubscription.DoesNotExist:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Email not found. Please subscribe first.",
                }
            )

        if subscription.is_verified:
            return JsonResponse(
                {"success": False, "message": "This email is already verified"}
            )

        # Generate new code and send email
        subscription.generate_verification_code()

        subject = "New Verification Code - COVU Marketplace"
        html_message = render_to_string(
            "coming_soon.html",
            {
                "verification_code": subscription.verification_code,
                "email": email,
                "is_email": True,
            },
        )
        plain_message = strip_tags(html_message)

        try:
            send_mail(
                subject=subject,
                message=plain_message,
                html_message=html_message,
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
            )
            return JsonResponse(
                {"success": True, "message": "New verification code sent to your email"}
            )
        except Exception as e:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Failed to send verification email. Please try again.",
                }
            )

    except json.JSONDecodeError as e:
        return JsonResponse(
            {
                "success": False,
                "message": f"Invalid request format: {str(e)}",
                "debug": str(e),
            }
        )
    except Exception as e:
        import traceback

        return JsonResponse(
            {
                "success": False,
                "message": f"An error occurred: {str(e)}",
                "debug": traceback.format_exc(),
            }
        )
