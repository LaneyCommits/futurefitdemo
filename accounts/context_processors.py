"""Context processors for accounts app."""
from .models import Profile


def user_profile(request):
    """
    Add user_profile to the template context when available.

    Profiles are now created at signup/login, even before email verification,
    but we still guard against older accounts that may not have one yet.
    """
    if request.user.is_authenticated:
        try:
            return {'user_profile': request.user.profile}
        except Profile.DoesNotExist:
            pass
    return {'user_profile': None}
