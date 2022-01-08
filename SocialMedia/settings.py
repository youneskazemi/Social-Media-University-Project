from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-galmq3jmq*l5xdwvh^pu3&$u0j!4_h66kk(u^4889(n)mv-l-7'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local apps
    'accounts.apps.AccountsConfig',
    'core.apps.CoreConfig',
    # Third-party apps
    'social_django',
    'storages',
    'sorl.thumbnail',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SocialMedia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SocialMedia.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'SM-Uni',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Substituting a custom User model
AUTH_USER_MODEL = 'accounts.User'

# CUSTOM AUTHENTICATION
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'accounts.authenticated.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',

]

# Oath AUTHENTICATION GOOGLE SETTINGS
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '613075060213-liuk9aanalkvjaq3uc4chbb4d6497mnc.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'http://127.0.0.1:8000'
SOCIAL_AUTH_USER_MODEL = 'accounts.User'

# ARVAN CLOUD

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_ACCESS_KEY_ID = '85ff0b31-d967-4645-bc6f-b7aac0730504'
AWS_S3_SECRET_ACCESS_KEY = '2f6077ec7582a46a7dcd8d7834b84fdd394510230af209e71b2d6a9797050a78'
AWS_STORAGE_BUCKET_NAME = 'paradox-uni'
AWS_S3_ENDPOINT_URL = 'https://s3.ir-thr-at1.arvanstorage.com'

# Email Setting
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sadknight78@gmail.com'
EMAIL_HOST_PASSWORD = 'qrnjszmngfbdzqlv'
