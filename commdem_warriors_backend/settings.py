"""
Django settings for commdem_warriors_backend project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

import gtts

# translated_text = translator.translate('Hi tanu, please listen to me I know yesterday was tough day for you, but I just want you to ask yourself that do I really dont have 20 min to do exercise ?',dest='bn')
tts = gtts.gTTS('hello sir, can I show you flow of features in our application ?',lang = 'en',slow=False,tld='co.in')
tts.save("static/hello1.mp3")

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'commitment',
    'rest_framework',
    'subscription',
    'designation',
    'cities',
    'income',
    'redeemPoints',
    'referralCode',
    'notifications',
    'location',
    'graphene_django',
    'food',
    'voiceAssistant',
    'background_task'
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

ROOT_URLCONF = 'commdem_warriors_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            }
        },
    },
]

WSGI_APPLICATION = 'commdem_warriors_backend.wsgi.application'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASE_ROUTERS = [
    # 'commitment.commitmentRouter.CommitmentRouter',
    # 'cities.citiesRouter.CitiesRouter',
    # 'designation.designationRouter.DesignationRouter',
    # 'income.incomeRouter.IncomeRouter',
    # 'location.locationRouter.LocationRouter',
    # 'redeemPoints.redeemPointsRouter.RedeemPointsRouter',
    # 'referralCode.referralCodeRouter.ReferralCodeRouter',
    # 'subscription.subscriptionRouter.SubscriptionRouter',
    # 'user.userRouter.UserRouter',
    ]
DATABASE_APPS_MAPPING = {
    # 'commitment': 'commitment_db',
    # 'designation':'designation_db',
    # 'income':'income_db',
    # 'location':'location_db',
    # 'notifications':'notifications_db',
    # 'redeemPoints':'redeemPoints_db',
    # 'referralCode':'referralCode_db',
    # 'subscription':'subscription_db',
    # 'user':'user_db',
    }

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE'),
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    },
    # 'commitment_db': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'commitment',
    #     'USER': 'postgres',
    #     'PASSWORD': '123',
    #     'HOST': '',
    #     'PORT': '',
    # },
    # 'designation_db': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'designation',
    #     'USER': 'postgres',
    #     'PASSWORD': '123',
    #     'HOST': '',
    #     'PORT': '',
    # },
    # 'income_db': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'income',
    #     'USER': 'postgres',
    #     'PASSWORD': '123',
    #     'HOST': '',
    #     'PORT': '',
    # },
    # 'location_db': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'location',
    #     'USER': 'postgres',
    #     'PASSWORD': '123',
    #     'HOST': '',
    #     'PORT': '',
    # },
    # 'notifications_db': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'notifications',
    #     'USER': 'postgres',
    #     'PASSWORD': '123',
    #     'HOST': '',
    #     'PORT': '',
    # },
    # 'redeemPoints_db': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'redeemPoints',
    #     'USER': 'postgres',
    #     'PASSWORD': '123',
    #     'HOST': '',
    #     'PORT': '',
    # },
    # 'referralCode_db': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'referralCode',
    #     'USER': 'postgres',
    #     'PASSWORD': '123',
    #     'HOST': '',
    #     'PORT': '',
    # },
    # 'subscription_db': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'subscription',
    #     'USER': 'postgres',
    #     'PASSWORD': '123',
    #     'HOST': '',
    #     'PORT': '',
    # },
    # 'user_db': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'user',
    #     'USER': 'postgres',
    #     'PASSWORD': '123',
    #     'HOST': '',
    #     'PORT': '',
    # }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaS  cript, Images)
# All settings common to all environments
# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

STATIC_ROOT = 'commdem_warriors_django/static'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# TIME_ZONE =  'Asia/Kolkata'