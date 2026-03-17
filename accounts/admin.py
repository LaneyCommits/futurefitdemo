from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Profile, EmailVerification

User = get_user_model()

# Replace the default registration so we can customize the user admin
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0
    verbose_name_plural = "Profile (email verification & personalization)"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Extend the built-in User admin so staff can see/manage all users,
    and quickly check whether their email is verified.
    """

    inlines = [ProfileInline]

    list_display = BaseUserAdmin.list_display + ("email", "is_active", "email_verified_status")
    list_filter = BaseUserAdmin.list_filter + ("is_active",)
    search_fields = BaseUserAdmin.search_fields + ("email",)

    def email_verified_status(self, obj):
        """
        Show whether this user's email has been verified.

        A checkmark means the user has a Profile with email_verified=True.
        A cross means they have not completed verification yet.
        """
        try:
            return bool(obj.profile.email_verified)
        except Profile.DoesNotExist:
            return False

    email_verified_status.boolean = True
    email_verified_status.short_description = "Email verified?"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "email_verified", "base_style")
    list_filter = ("email_verified", "base_style")
    search_fields = ("user__username", "user__email")


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "key", "created_at")
    search_fields = ("user__username", "user__email", "key")
    readonly_fields = ("created_at",)
    help_texts = {
        "user": "The user this verification link was generated for.",
        "key": "One-time token included in the verification URL that is emailed to the user.",
    }

