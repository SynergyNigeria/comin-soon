from django.db import models
from django.utils import timezone
import uuid


class EmailSubscription(models.Model):
    """Model to store email subscriptions for the coming soon page"""

    email = models.EmailField(unique=True, help_text="Subscriber's email address")
    subscribed_at = models.DateTimeField(
        default=timezone.now, help_text="When the user subscribed"
    )
    is_verified = models.BooleanField(
        default=False, help_text="Whether the email has been verified"
    )
    verification_code = models.CharField(
        max_length=6, blank=True, null=True, help_text="6-digit verification code"
    )
    code_expires_at = models.DateTimeField(
        blank=True, null=True, help_text="When the verification code expires"
    )
    verification_attempts = models.PositiveIntegerField(
        default=0, help_text="Number of verification attempts"
    )

    class Meta:
        ordering = ["-subscribed_at"]
        verbose_name = "Email Subscription"
        verbose_name_plural = "Email Subscriptions"

    def __str__(self):
        return f"{self.email} - {'Verified' if self.is_verified else 'Unverified'}"

    def generate_verification_code(self):
        """Generate a new 6-digit verification code"""
        import random

        self.verification_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        self.code_expires_at = timezone.now() + timezone.timedelta(
            minutes=10
        )  # Code expires in 10 minutes
        self.verification_attempts = 0
        self.save()

    def is_code_valid(self, code):
        """Check if the provided code is valid"""
        if not self.verification_code or not self.code_expires_at:
            return False

        if timezone.now() > self.code_expires_at:
            return False

        if self.verification_attempts >= 5:  # Max 5 attempts
            return False

        return self.verification_code == code

    def increment_attempts(self):
        """Increment verification attempts counter"""
        self.verification_attempts += 1
        self.save()

    def verify_email(self):
        """Mark email as verified"""
        self.is_verified = True
        self.verification_code = None
        self.code_expires_at = None
        self.save()
