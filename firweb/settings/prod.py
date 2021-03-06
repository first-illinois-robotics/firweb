import os
import io

import environ  # type: ignore
from google.cloud import secretmanager
from google.cloud.secretmanager_v1 import SecretManagerServiceClient

from .common import BASE_DIR

# Imports the Cloud Logging client library
import google.cloud.logging

# Instantiates a client
client = google.cloud.logging.Client()

# Retrieves a Cloud Logging handler based on the environment
# you're running in and integrates the handler with the
# Python logging module. By default this captures all logs
# at INFO level and higher
client.setup_logging()

env = environ.Env()
env_file = os.path.join(BASE_DIR, ".env")

project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

if os.path.isfile(env_file):
    # Use a local secret file, if provided
    env.read_env(env_file)
else:
    secret_client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = secret_client.access_secret_version(name=name).payload.data.decode(
        "UTF-8"
    )

    env.read_env(io.StringIO(payload))

DEBUG = False

SECRET_KEY = env("SECRET_KEY")

DATABASES = {
    "default": env.db(),
}

# temporary fix for django-environ bug
# see https://github.com/joke2k/django-environ/issues/294
if "/" in DATABASES["default"]["NAME"]:
    DATABASES["default"]["HOST"], DATABASES["default"]["NAME"] = DATABASES["default"][
        "NAME"
    ].rsplit("/", 1)

if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432

DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_BUCKET_NAME = env.str("GS_BUCKET_NAME")
GS_QUERYSTRING_AUTH = False

DJANGOCMS_GOOGLEMAP_API_KEY = env.str("GMAPS_API")

# ONLY safe if deploying through GAE. If deploying elsewhere, this must be modified
ALLOWED_HOSTS = ["*"]

# Various security settings
# see https://www.django-cms.org/en/blog/2022/02/22/security-enhancements-for-django-cms/

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

SECURE_HSTS_SECONDS = 31536000  # 1 Year
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = True

CMS_TOOLBAR_ANONYMOUS_ON = False

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

GOOGLE_TAG_ID = env.str("GOOGLE_MEASUREMENT_ID", None)

# redefining entire template object so we can enable cached templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "firweb", "templates"),
        ],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.csrf",
                "django.template.context_processors.tz",
                "sekizai.context_processors.sekizai",
                "django.template.context_processors.static",
                "cms.context_processors.cms_settings",
                "firweb.context_processors.program",
            ],
            "loaders": [
                ("django.template.loaders.cached.Loader", [
                    "django.template.loaders.filesystem.Loader",
                    "django.template.loaders.app_directories.Loader"
                ])
            ],
        },
    },
]

if not os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    CACHES = {
        "default": {
            "BACKEND": "firweb.backends.GaeMemcachedCache",
        }
    }

    # Done to avoid cache invalidation at runtime which will fail
    CMS_PAGE_CACHE = False

    EMAIL_BACKEND = "firweb.backends.GaeMailBackend"
    DEFAULT_FROM_EMAIL = "noreply@firstillinoisrobotics.org"
