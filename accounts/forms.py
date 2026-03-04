"""Custom auth forms with username rules and email; profile and personalization."""
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Profile


USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_.]+\Z')
USERNAME_MAX_LENGTH = 20


class CustomUserCreationForm(UserCreationForm):
    """Signup form: username max 20 chars, only letters, numbers, _ and .; email required."""

    email = forms.EmailField(
        required=True,
        label='Email',
        help_text='We’ll send a verification link to this address.',
    )

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].max_length = USERNAME_MAX_LENGTH
        self.fields['username'].widget.attrs['maxlength'] = str(USERNAME_MAX_LENGTH)
        self.fields['username'].help_text = ''  # remove default "@/./+/-/_ only" text

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        if len(username) > USERNAME_MAX_LENGTH:
            raise ValidationError(
                f'Username must be {USERNAME_MAX_LENGTH} characters or fewer.',
                code='username_too_long',
            )
        if not USERNAME_PATTERN.match(username):
            raise ValidationError(
                'Username can only contain letters, numbers, underscores (_) and periods (.).',
                code='username_invalid',
            )
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].strip().lower()
        if commit:
            user.save()
            self.save_m2m()
        return user


class ProfileUpdateForm(forms.ModelForm):
    """Profile avatar and bio."""

    class Meta:
        model = Profile
        fields = ('avatar', 'bio')

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and avatar.size > 2 * 1024 * 1024:  # 2 MB
            raise ValidationError('Image must be under 2 MB.')
        return avatar


class PersonalizationForm(forms.ModelForm):
    """AI style and custom instructions."""

    class Meta:
        model = Profile
        fields = ('base_style', 'custom_instructions')
        widgets = {
            'custom_instructions': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'e.g. Write like a real human. Stay professional but casual. Avoid buzzwords and jargon.',
            }),
        }
