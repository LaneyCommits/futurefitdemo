"""
Django settings for Project7 project.
"""
import os
from pathlib import Path
 



BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env from project root (e.g. SECRET_KEY, DEBUG)
from dotenv import load_dotenv
load_dotenv(BASE_DIR / '.env')





SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-me-in-production')

DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Public site URL (https://yourdomain.com) — used for SEO canonical URLs, sitemap, and JSON-LD.
SITE_PUBLIC_URL = (os.environ.get("site_url") or "").strip().rstrip("/")

CSRF_TRUSTED_ORIGINS = []
if os.getenv("site_url"):
    ALLOWED_HOSTS.append(os.getenv("site_url").replace("https://", "").replace("http://", "").split("/")[0])
    CSRF_TRUSTED_ORIGINS.append(os.getenv("site_url").rstrip("/"))

# Extra hosts (comma-separated), e.g. DigitalOcean App Platform or custom domain
_extra_hosts = os.environ.get("ALLOWED_HOSTS", "")
if _extra_hosts.strip():
    ALLOWED_HOSTS.extend([h.strip() for h in _extra_hosts.split(",") if h.strip()])

_extra_csrf = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
if _extra_csrf.strip():
    for _o in _extra_csrf.split(","):
        _o = _o.strip()
        if _o and _o not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(_o)

# Optional: Google Search Console HTML tag verification (content token only).
GOOGLE_SITE_VERIFICATION = os.environ.get("GOOGLE_SITE_VERIFICATION", "").strip()


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'resume_analysis',
    'career_quiz',
    'resume',
    'schools',
    'blog',
    'accounts',
    'chat',
    'jobs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
]
# WhiteNoise only when DEBUG=False (Gunicorn in production). With DEBUG=True, runserver
# serves /static/ via django.contrib.staticfiles — WhiteNoise in front often breaks local CSS.
if not DEBUG:
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')
MIDDLEWARE.extend([
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
])

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.user_profile',
                'config.context_processors.site_seo',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if os.environ.get("DATABASE_URL"):
    import dj_database_url
    DATABASES["default"] = dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Leading slash so {% static %} URLs are always rooted at /static/... (not relative to current path)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Email (verification, etc.)
# Default: console backend prints the verification link to the terminal (no real email sent).
# To send real emails, set in .env:
#   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
#   EMAIL_HOST=smtp.gmail.com
#   EMAIL_PORT=587
#   EMAIL_USE_TLS=True
#   EMAIL_HOST_USER=your@gmail.com
#   EMAIL_HOST_PASSWORD=your-app-password
# (Gmail: use an App Password, not your normal password.)
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'ExploringU <noreply@exploringu.example.com>')
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'true').lower() in ('true', '1', 'yes')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# Avoid failed SMTP (500 on signup) when .env still has example Gmail placeholders.
if (
    'smtp' in EMAIL_BACKEND.lower()
    and (
        EMAIL_HOST_USER.strip() in ('', 'your@gmail.com', 'you@example.com')
        or EMAIL_HOST_PASSWORD.strip() in ('', 'your-app-password', 'your-password')
    )
):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Production (Docker / DigitalOcean App Platform)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'true').lower() in ('true', '1', 'yes')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
