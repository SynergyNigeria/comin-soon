"""
Email sending utilities with multiple backend support.
Supports Resend API (recommended for hosting platforms) and SMTP fallback.
"""

import os
import requests
from django.core.mail import send_mail
from django.conf import settings


def send_email_with_resend(subject, html_content, plain_content, recipient_email):
    """
    Send email using Resend API (https://resend.com)
    Free tier: 3,000 emails/month, 100 emails/day
    """
    resend_api_key = os.environ.get("RESEND_API_KEY")
    
    if not resend_api_key:
        raise Exception("RESEND_API_KEY not set in environment variables")
    
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {resend_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": os.environ.get("RESEND_FROM_EMAIL", "COVU <onboarding@resend.dev>"),
        "to": [recipient_email],
        "subject": subject,
        "html": html_content,
        "text": plain_content
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    
    if response.status_code == 200:
        print(f"Email sent successfully via Resend to {recipient_email}")
        return True
    else:
        error_msg = response.json().get("message", "Unknown error")
        raise Exception(f"Resend API error: {error_msg} (Status: {response.status_code})")


def send_email_with_smtp(subject, html_content, plain_content, recipient_email):
    """
    Send email using SMTP (fallback method)
    """
    send_mail(
        subject=subject,
        message=plain_content,
        html_message=html_content,
        from_email=None,
        recipient_list=[recipient_email],
        fail_silently=False,
    )
    print(f"Email sent successfully via SMTP to {recipient_email}")


def send_verification_email(recipient_email, verification_code):
    """
    Send verification email using the best available method.
    Tries Resend API first, falls back to SMTP if needed.
    """
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    
    subject = "Verify Your Email - COVU Marketplace"
    html_content = render_to_string(
        "coming_soon.html",
        {
            "verification_code": verification_code,
            "email": recipient_email,
            "is_email": True,
        },
    )
    plain_content = strip_tags(html_content)
    
    # Try Resend API first (recommended for hosting platforms)
    if os.environ.get("RESEND_API_KEY"):
        try:
            send_email_with_resend(subject, html_content, plain_content, recipient_email)
            return True
        except Exception as e:
            print(f"Resend API failed: {str(e)}, trying SMTP...")
            # Fall through to SMTP
    
    # Fallback to SMTP
    try:
        send_email_with_smtp(subject, html_content, plain_content, recipient_email)
        return True
    except Exception as e:
        print(f"SMTP also failed: {str(e)}")
        raise Exception(f"Failed to send email via both Resend and SMTP: {str(e)}")
