from django.contrib import admin
from .models import EmailSubscription


@admin.register(EmailSubscription)
class EmailSubscriptionAdmin(admin.ModelAdmin):
    """Admin interface for Email Subscriptions"""

    list_display = [
        "email",
        "is_verified",
        "subscribed_at",
        "verification_attempts",
        "code_status",
    ]

    list_filter = ["is_verified", "subscribed_at", "verification_attempts"]

    search_fields = ["email"]

    readonly_fields = [
        "subscribed_at",
        "verification_code",
        "code_expires_at",
        "verification_attempts",
    ]

    ordering = ["-subscribed_at"]

    def code_status(self, obj):
        """Display verification code status"""
        if obj.is_verified:
            return "✅ Verified"
        elif obj.code_expires_at:
            from django.utils import timezone

            if timezone.now() > obj.code_expires_at:
                return "⏰ Expired"
            return "⏳ Active"
        return "❌ No Code"

    code_status.short_description = "Code Status"

    fieldsets = (
        ("Email Information", {"fields": ("email", "is_verified", "subscribed_at")}),
        (
            "Verification Details",
            {
                "fields": (
                    "verification_code",
                    "code_expires_at",
                    "verification_attempts",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ["mark_as_verified", "mark_as_unverified"]

    def mark_as_verified(self, request, queryset):
        """Action to manually verify emails"""
        count = queryset.update(
            is_verified=True, verification_code=None, code_expires_at=None
        )
        self.message_user(request, f"{count} email(s) marked as verified.")

    mark_as_verified.short_description = "Mark selected emails as verified"

    def mark_as_unverified(self, request, queryset):
        """Action to mark emails as unverified"""
        count = queryset.update(is_verified=False)
        self.message_user(request, f"{count} email(s) marked as unverified.")

    mark_as_unverified.short_description = "Mark selected emails as unverified"
