from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-(j(kn3r)u2w#!5yn4$rh@!9jc0&j5cn$_sggxbr322o2!chfph'
DEBUG = True
ALLOWED_HOSTS = []
AUTH_USER_MODEL = 'actounts_app.CustomUser'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'classifier_app',
    'actounts_app',
    'news_app',
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
ROOT_URLCONF = 'FakeNewsClassifier.urls'
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
                'django.contrib.messages.context_processors.messages',],},},]
WSGI_APPLICATION = 'FakeNewsClassifier.wsgi.application'
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'bg-blue-100 border-blue-400 text-blue-700',
    messages.INFO: 'bg-blue-100 border-blue-400 text-blue-700',
    messages.SUCCESS: 'bg-green-100 border-green-400 text-green-700',
    messages.WARNING: 'bg-yellow-100 border-yellow-400 text-yellow-700',
    messages.ERROR: 'bg-red-100 border-red-400 text-red-700',
}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fake_news_classifier_db',
        'USER': 'ujjal',
        'PASSWORD': 'ujjal123',
        'HOST': 'localhost',
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
USE_TZ = True
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
NEWS_API_KEY = '658d11dc84764ff1b23f9a28bd7a3ae5'