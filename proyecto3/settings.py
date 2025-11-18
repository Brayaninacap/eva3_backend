"""
Configuración de Django para proyecto 'proyecto3'.

Generado por 'django-admin startproject' usando Django 5.0.

Para obtener más información sobre este archivo, consulta
https://docs.djangoproject.com/en/5.0/topics/settings/

Para obtener la lista completa de configuraciones, consulta
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# Construye rutas dentro del proyecto como: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Configuración de seguridad
# ADVERTENCIA: ¡Mantén la clave secreta utilizada en producción en secreto!
SECRET_KEY = 'django-insecure-j_#p&o8z-@!0h9z9_#p&o8z-@!0h9z9_#p&o8z-@!0h9z9_#p&o8z-@!0h9z9'

# ADVERTENCIA: ¡No lo ejecutes con DEBUG = True en producción!
DEBUG = True

ALLOWED_HOSTS = []


# Definición de las aplicaciones
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ------------------------------------
    # Agregamos nuestra aplicación 'app'
    'app',
    # ------------------------------------
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

ROOT_URLCONF = 'proyecto3.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Agregamos la ruta base de plantillas del proyecto (opcional)
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
        'APP_DIRS': True, # Busca templates dentro de cada carpeta 'templates' de las apps
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

WSGI_APPLICATION = 'proyecto3.wsgi.application'


# Base de datos
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Validadores de contraseña
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internacionalización
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-es' # Usamos español

TIME_ZONE = 'America/Santiago' # Ajusta tu zona horaria si es diferente

USE_I18N = True

USE_TZ = True


# Archivos estáticos (CSS, JS, Imágenes)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Tipo de campo clave primaria por defecto
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'