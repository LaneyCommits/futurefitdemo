"""Auth views: login, signup, logout, email verification, profile, personalization."""
import logging
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse

from .forms import CustomUserCreationForm, ProfileUpdateForm, PersonalizationForm
from .models import Profile, EmailVerification

logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        # No profile until email is verified; send unverified users to check-email page
        try:
            self.request.user.profile
        except Profile.DoesNotExist:
            return reverse_lazy('verify_email_sent')
        return reverse_lazy('home')


def _send_verification_email(request, user, verification):
    """Send email with verification link."""
    verify_url = request.build_absolute_uri(
        reverse('verify_email', kwargs={'key': verification.key})
    )
    subject = 'Verify your ExploringU email'
    message = (
        f'Hi {user.username},\n\n'
        f'Please verify your email by clicking the link below:\n\n'
        f'{verify_url}\n\n'
        f'This link is valid for 24 hours. If you didn\'t create an account, you can ignore this email.\n\n'
        f'— ExploringU'
    )
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@exploringu.example.com')
    try:
        send_mail(
            subject,
            message,
            from_email,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        logger.exception('Failed to send verification email: %s', e)


def signup_view(request):
    """Sign up new users; send verification email. Profile is created only after email verification."""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            verification = EmailVerification.create_for_user(user)
            _send_verification_email(request, user, verification)
            login(request, user)
            return redirect('verify_email_sent')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def verify_email_sent_view(request):
    """Shown after signup: check your email for the verification link."""
    return render(request, 'accounts/verify_email_sent.html')


def verify_email_view(request, key):
    """Verify email from link; create profile only here (profile is not created until email is verified)."""
    verification = get_object_or_404(EmailVerification, key=key)
    Profile.objects.get_or_create(user=verification.user, defaults={'email_verified': True})
    verification.delete()
    return redirect('verify_email_done')


def verify_email_done_view(request):
    """Shown after successful verification."""
    return render(request, 'accounts/verify_email_done.html')


class CustomLogoutView(LogoutView):
    next_page = 'home'


@login_required
def profile_view(request):
    """View and edit profile: avatar, bio. Requires verified email (profile exists)."""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('verify_email_sent')
    quiz_labels = []
    try:
        quiz_labels = request.user.quiz_result.pill_labels or []
    except Exception:
        pass
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'form': form,
        'quiz_pill_labels': quiz_labels,
    })


@login_required
def personalization_view(request):
    """View and edit AI personalization: base style, custom instructions. Requires verified email."""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('verify_email_sent')
    if request.method == 'POST':
        form = PersonalizationForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('personalization')
    else:
        form = PersonalizationForm(instance=profile)
    return render(request, 'accounts/personalization.html', {
        'profile': profile,
        'form': form,
    })
