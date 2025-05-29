from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-!vsg!3+q7m^nr9@#b(6%7u0t^ca8z&sc0#uh^#i5e#m6jkc(pm'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',

    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',

    'accounts',            # CustomUser y lógica de autenticación (además de nutricionistas si decides agruparlos)
    'invitations',         # Gestión de invitaciones
    'nutrition_plans',     # Planes nutricionales
    'nutritionists',       # Opcional: perfil específico del nutricionista (si decides separarlo)
    'patients',            # Perfiles y datos propios de pacientes
    'progress_tracking',   # Registros de progreso y métricas
    'appointments'
]

CRONJOBS = [
  # Ejecuta a las 9:00 cada día
  ("0 9 * * *", "appointments.cron.send_reminders")
]

MIDDLEWARE = [
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'NutritionApp_v1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Ubicación de tus plantillas HTML (si las usas)
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',  # Necesario para algunas funcionalidades de DRF o admin
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'NutritionApp_v1.wsgi.application'

# PostgreSQL Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nutrition_app',           # Cambia este valor al nombre de tu base de datos
        'USER': 'admin_nutrition',         # Cambia este valor a tu usuario de PostgreSQL
        'PASSWORD': 'adnut2106b',          # Cambia este valor a la contraseña correspondiente
        'HOST': 'localhost',               # Generalmente "localhost", o el IP/host de tu servidor de BD
        'PORT': '5432',                    # Puerto por defecto de PostgreSQL
    }
}

# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Dirección del servidor SMTP (ejemplo usando Gmail)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))

# Credenciales SMTP
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'geriguti09@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'fsdv nsjo eunz hsob')

# Seguridad de la conexión
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False') == 'True'

# Dirección que aparecerá en el From de los correos salientes
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'no-reply@tudominio.com')

# Configuración CORS (opcional)
CORS_ALLOW_ALL_ORIGINS = True


