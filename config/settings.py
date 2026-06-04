"""
Django settings for config project.
Security-hardened configuration — DevSecOps & Compliance Analyst pass.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
import cloudinary

# Ensure Django loads your .env variables
load_dotenv()

# Initialize Cloudinary SDK with credentials
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# CORE SECURITY
# ---------------------------------------------------------------------------

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-insecure-key-for-local-only')

DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ---------------------------------------------------------------------------
# INSTITUTIONAL EMAIL RESTRICTION
# Only accounts with this email domain are permitted to register.
# Override via ALLOWED_EMAIL_DOMAIN env var for other deployments.
# ---------------------------------------------------------------------------
ALLOWED_EMAIL_DOMAIN = os.getenv('ALLOWED_EMAIL_DOMAIN', 'evsu.edu.ph')

# ---------------------------------------------------------------------------
# APPLICATION DEFINITION
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # --- project apps ---
    'research_repo',
    'publication_api',
    # --- cloud storage ---
    'cloudinary_storage',
    'cloudinary',
    # --- REST ---
    'rest_framework',
    # --- security packages ---
    'axes',          # Task 1: brute-force protection
    'honeypot',      # Task 2: honeypot fields
    'csp',           # Task 6: Content-Security-Policy header
    # --- custom DevSecOps module ---
    'security.apps.SecurityConfig',
]

print(f"DEBUG: Cloud Name is {os.getenv('CLOUDINARY_CLOUD_NAME')}")

# ---------------------------------------------------------------------------
# MIDDLEWARE  (order matters — axes near the top, after sessions & auth)
# ---------------------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'axes.middleware.AxesMiddleware',                          # Task 1 – must come after AuthenticationMiddleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',                            # Task 6 – CSP header
    'django_permissions_policy.PermissionsPolicyMiddleware',  # Task 6 – Permissions-Policy header
    'security.middleware.AuditLogMiddleware',                  # Task 3 – custom audit logger
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}

WSGI_APPLICATION = 'config.wsgi.application'

# ---------------------------------------------------------------------------
# DATABASE
# ---------------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------------------------------

AUTH_USER_MODEL = 'research_repo.User'

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',  # Task 1 – axes must be first
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------------------------------------------
# REST FRAMEWORK
# ---------------------------------------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },
}

# ---------------------------------------------------------------------------
# TASK 1 — BRUTE-FORCE PROTECTION (django-axes)
# ---------------------------------------------------------------------------

AXES_ENABLED = True
AXES_FAILURE_LIMIT = 5                    # lock after 5 consecutive failures
AXES_COOLOFF_TIME = 1                     # unlock after 1 hour (timedelta or int hours)
AXES_LOCK_OUT_AT_FAILURE = True
AXES_LOCKOUT_CALLABLE = None              # use default HTTP 403 lockout response
AXES_RESET_ON_SUCCESS = True             # reset counter on successful login
AXES_LOCKOUT_PARAMETERS = [             # lock by combination of IP + username
    ['ip_address', 'username'],
]
AXES_IPWARE_PROXY_COUNT = 0              # adjust if behind a reverse proxy
AXES_VERBOSE = True
AXES_LOCKOUT_TEMPLATE = None            # let middleware return 403
AXES_NEVER_LOCKOUT_WHITELIST = False

# ---------------------------------------------------------------------------
# TASK 2 — HONEYPOT (django-honeypot)
# ---------------------------------------------------------------------------

HONEYPOT_FIELD_NAME = 'phone_number'     # hidden field name bots fill in
HONEYPOT_VALUE = ''                      # expected value is empty

# ---------------------------------------------------------------------------
# TASK 3 — AUDIT LOGGING  (see security/audit_logger.py)
# ---------------------------------------------------------------------------

LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'json_audit': {
            '()': 'security.formatters.JSONAuditFormatter',
        },
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {message}',
            'style': '{',
        },
    },

    'handlers': {
        'audit_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'audit.log'),
            'maxBytes': 10 * 1024 * 1024,   # 10 MB
            'backupCount': 10,
            'formatter': 'json_audit',
            'encoding': 'utf-8',
        },
        'security_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'security.log'),
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'json_audit',
            'encoding': 'utf-8',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },

    'loggers': {
        'security.audit': {
            'handlers': ['audit_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'security.brute_force': {
            'handlers': ['security_file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'security.honeypot': {
            'handlers': ['security_file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'axes': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# ---------------------------------------------------------------------------
# TASK 6 — HTTP SECURITY HEADERS
# ---------------------------------------------------------------------------

# --- Strict-Transport-Security ---
SECURE_HSTS_SECONDS = 31536000          # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# --- SSL redirect (enable in production) ---
SECURE_SSL_REDIRECT = not DEBUG

# --- Cookie security ---
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 3600               # 1 hour session timeout

CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# --- Misc ---
SECURE_CONTENT_TYPE_NOSNIFF = True      # X-Content-Type-Options: nosniff
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'               # X-Frame-Options

# --- Referrer-Policy ---
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# --- Content-Security-Policy (django-csp 4.0 format) ---
# In dev (DEBUG=True): report-only mode. In prod: enforcing mode.
_CSP_DIRECTIVES = {
    'default-src': ("'self'",),
    'script-src': ("'self'",),
    'style-src': ("'self'", "'unsafe-inline'"),   # inline styles needed by Django admin
    'img-src': ("'self'", "data:", "res.cloudinary.com", "*.cloudinary.com"),
    'font-src': ("'self'",),
    'connect-src': ("'self'",),
    'frame-ancestors': ("'none'",),
    'form-action': ("'self'",),
    'base-uri': ("'none'",),
    'object-src': ("'none'",),
}

if DEBUG:
    CONTENT_SECURITY_POLICY_REPORT_ONLY = {'DIRECTIVES': _CSP_DIRECTIVES}
else:
    CONTENT_SECURITY_POLICY = {'DIRECTIVES': _CSP_DIRECTIVES}

# --- Permissions-Policy (django-permissions-policy) ---
PERMISSIONS_POLICY = {
    'accelerometer': [],
    'camera': [],
    'geolocation': [],
    'gyroscope': [],
    'magnetometer': [],
    'microphone': [],
    'payment': [],
    'usb': [],
}

# ---------------------------------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# STATIC & MEDIA FILES
# ---------------------------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
