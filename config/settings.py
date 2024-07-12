import os
from pathlib import Path

from decouple import config

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'verbose': {
			'format': '{levelname} {asctime} {module} {message}',
			'style': '{',
		},
		'simple': {
			'format': '{levelname} {message}',
			'style': '{',
		},
	},
	'handlers': {
		'console': {
			'class': 'logging.StreamHandler',
			'formatter': 'simple',
		},
		'file': {
			'level': 'DEBUG',
			'class': 'logging.FileHandler',
			'filename': 'debug.log',
			'formatter': 'verbose',
		},
	},
	'root': {
		'handlers': ['console', 'file'],
		'level': 'DEBUG',
	},
}

USE_TZ = True
USE_I18N = True
LANGUAGE_CODE = "en-us"
ROOT_URLCONF = "config.urls"
AUTH_USER_MODEL = "user.User"
WSGI_APPLICATION = "config.wsgi.application"
TIME_ZONE = config("TIME_ZONE", default="UTC")
DEBUG = config("DEBUG", cast=bool, default=True)
BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "apps"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SECRET_KEY = config("SECRET_KEY", default="secret-key-!!!")
AUTHENTICATION_BACKENDS = ["apps.user.backend.ModelBackend"]

ALLOWED_HOSTS = (
	["*"]
	if DEBUG
	else config(
		"ALLOWED_HOSTS", cast=lambda host: [h.strip() for h in host.split(",") if h]
	)
)

AUTH_PASSWORD_VALIDATORS = [
	{
		"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
	},
	{"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
	{"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
	{"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

MIDDLEWARE = [
	"django.middleware.security.SecurityMiddleware",
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
	"django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
	{
		"BACKEND": "django.template.backends.django.DjangoTemplates",
		"DIRS": [BASE_DIR / "templates"],
		"APP_DIRS": True,
		"OPTIONS": {
			"context_processors": [
				"django.template.context_processors.debug",
				"django.template.context_processors.request",
				"django.contrib.auth.context_processors.auth",
				"django.contrib.messages.context_processors.messages",
			],
		},
	},
]

# Applications
APPLICATIONS = ["user", "core", "products", "buy"]

INSTALLED_APPS = [
	"jazzmin",
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",
	# Third-party
	"rest_framework",
	"django_celery_beat",
	"multiupload",
	"crispy_forms",
	"crispy_tailwind",
	"taggit",
	# Application
	*list(map(lambda app: f"apps.{app}", APPLICATIONS)),
]

# Form Design
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Serving
STATIC_URL = "static/"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "storage/media"

# celery
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_DEFAULT_QUEUE = "default"

# logout / login
LOGIN_URL = "signin"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "signin"

# Mode Handling:
if DEBUG:
	STATICFILES_DIRS = [BASE_DIR / "storage/static"]
	
	DATABASES = {
		"default": {
			"ENGINE": "django.db.backends.sqlite3",
			"NAME": BASE_DIR / "db.sqlite3",
		}
	}
	
	CACHES = {
		"default": {
			"BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
			"LOCATION": BASE_DIR / "tmp/cache",
		}
	}
	
	EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
	EMAIL_HOST = "smtp.gmail.com"
	EMAIL_PORT = 587
	EMAIL_USE_TLS = True
	EMAIL_USE_SSL = False
	EMAIL_HOST_USER = "django.Onlineshop@gmail.com"
	EMAIL_HOST_PASSWORD = "tzhc fkcz yfpj jlcq"
	DEFAULT_FROM_EMAIL = "amiraliqobadi379@gmail.com"


else:
	REDIS_URL = f"redis://{config('REDIS_HOST')}:{config('REDIS_PORT')}"
	
	DATABASES = {
		"default": {
			"ENGINE": "django.db.backends.postgresql",
			"NAME": config("DB_NAME"),
			"USER": config("DB_USER"),
			"PASSWORD": config("DB_PASSWORD"),
			"HOST": config("DB_HOST"),
			"PORT": config("DB_PORT"),
		}
	}
	
	CACHES = {
		"default": {
			"BACKEND": "django.core.cache.backends.redis.RedisCache",
			"LOCATION": REDIS_URL,
		}
	}
	
	EMAIL_USE_TLS = config("EMAIL_USE_TLS")
	EMAIL_USE_SSL = config("EMAIL_USE_SSL")
	EMAIL_HOST = config("EMAIL_HOST")
	EMAIL_PORT = config("EMAIL_PORT")
	EMAIL_HOST_USER = config("EMAIL_USER")
	EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
	DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
