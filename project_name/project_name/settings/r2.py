# R2 Hosting
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
THUMBNAIL_DEFAULT_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


# https://dash.cloudflare.com/(account id)/r2/api-tokens
AWS_ACCESS_KEY_ID = None # override in settings/local.py
AWS_SECRET_ACCESS_KEY = None # override in settings/local.py


# https://dash.cloudflare.com/(account id)/r2/new
AWS_STORAGE_BUCKET_NAME = "bucket-name"

# Bucket details, S3 API (up to slash)
AWS_S3_ENDPOINT_URL = (
    "https://(account id).r2.cloudflarestorage.com"
)
AWS_S3_SIGNATURE_VERSION = "s3v4"

# Bucket settings, Custom Domains
AWS_S3_CUSTOM_DOMAIN = "some-media-subdomain.cruncher.ch"
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
