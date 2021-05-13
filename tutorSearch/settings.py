"""
Django settings for tutorSearch project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django_heroku
from decouple import config
from ckeditor.configs import DEFAULT_CONFIG
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1zqb-ml)1hbr6+5+jpm89c_hwi(qx(+m8*$xn+)8)_klm1^eiw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['jdmr.herokuapp.com', 'localhost']
# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'channels',
    'chat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'rest_framework_api_key',
    'teacher',
    'students',
    'institute',
    'accounts',
    'dashboard',
    'courses',
    'batches',
    'fees',
    'tutorials',
    'results',
    'exams',
    'notes',
    'buy_items',
    'django_cleanup',

    'code2learn_app',
    'import_export',
    'rangefilter',
    'certificate',
    'users',
    'blog',
    'ckeditor',
    'ckeditor_uploader',
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

ROOT_URLCONF = 'tutorSearch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        }
    },
]

WSGI_APPLICATION = 'tutorSearch.wsgi.application'




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jdmr',
        'USER': 'postgres',
<<<<<<< HEAD
        'PASSWORD': 'Yash@2000',
=======
        'PASSWORD': 'Sandeep@99',
>>>>>>> 430aaddf74a524353d49a2fae30605ad6f65778c
        'HOST':'localhost',
        'PORT':'5432',
    },
}



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ASGI_APPLICATION = 'tutorSearch.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# Activate Django-Heroku.
django_heroku.settings(locals())


# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         # 'rest_framework.authentication.BasicAuthentication',
#         # 'rest_framework.authentication.SessionAuthentication',
#         'knox.auth.TokenAuthentication',
#     ]
# }
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# REST_FRAMEWORK = {
#     "DEFAULT_PERMISSION_CLASSES": [
#         "rest_framework_api_key.permissions.HasAPIKey",
#     ],
# }

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_MAIL_SUBJECT = "COACHING OTP"
EMAIL_HOST_PASSWORD = ''
EMAIL_PAGE_DOMAIN = 'localhost'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_MODEL_ADMIN = False

# paytm crads
# MERCHANT_KEY = config("PYTM_SECRET")
# MID = config("PYTM_ID")
MERCHANT_KEY = 'C&So29O%S3JYTS8A'
MID = 'sAxWIA43891172965346'

# razorpay

# KEY_ID = config("RZP_KEY_ID")
# KEY_SECRET = config("RZP_KEY_SECRET")
KEY_ID='rzp_live_knSYzxPqUNGQaL'
KEY_SECRET = 'Dy5B7Y2cTVLBnWkLi1mRlehH'

# CkEditor Configs
CKEDITOR_UPLOAD_PATH = "blog/uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
# CKEDITOR_THUMBNAIL_SIZE = (300, 300)
CKEDITOR_IMAGE_QUALITY = 40
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_ALLOW_NONIMAGE_FILES = True

CUSTOM_TOOLBAR = [
    {
        "name": "document",
        "items": [
            "Styles", "Format", "Bold", "Italic", "Underline", "Strike", "-",
            "TextColor", "BGColor",  "-",
            "JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock",
        ],
    },
    {
        "name": "widgets",
        "items": [
            "Undo", "Redo", "-",
            "NumberedList", "BulletedList", "-",
            "Outdent", "Indent", "-",
            "Link", "Unlink", "-",
            "Image", "CodeSnippet", "Table", "HorizontalRule", "Smiley", "SpecialChar", "-",
            "Blockquote", "-",
            "ShowBlocks", "Maximize",
        ],
    },
]

CKEDITOR_CONFIGS = {
    "default": DEFAULT_CONFIG,
    "my-custom-toolbar": {
        "skin": "moono-lisa",
        "toolbar": CUSTOM_TOOLBAR,
        "toolbarGroups": None,
        "extraPlugins": ",".join(["image2", "codesnippet"]),
        "removePlugins": ",".join(["image"]),
        "codeSnippet_theme": "xcode",
        "image2_alignClasses": ['align-left','align-center','align-right']
    },
}