"""Context processors for accounts app."""
from .models import Profile


def user_profile(request):
    """Add user_profile only when the user has a profile (created after email verification)."""
    if request.user.is_authenticated:
        try:
            return {'user_profile': request.user.profile}
        except Profile.DoesNotExist:
            pass
    return {'user_profile': None}
