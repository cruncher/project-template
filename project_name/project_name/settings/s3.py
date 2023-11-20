# CORS headers
"""
<?xml version="1.0" ?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedMethod>PUT</AllowedMethod>
    <AllowedMethod>POST</AllowedMethod>
    <AllowedHeader>*</AllowedHeader>
  </CORSRule>
</CORSConfiguration>
"""

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
THUMBNAIL_DEFAULT_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

AWS_STORAGE_BUCKET_NAME = ''
AWS_S3_REGION_NAME = 'ch-gva-2'
AWS_DEFAULT_ACL = 'public-read'
AWS_BUCKET_ACL = 'public-read'
AWS_AUTO_CREATE_BUCKET = True
AWS_S3_HOST = 'sos-ch-gva-2.exo.io'
AWS_S3_USE_SSL = True
AWS_S3_CUSTOM_DOMAIN = '%s.sos-ch-gva-2.exo.io' % AWS_STORAGE_BUCKET_NAME
AWS_S3_ENDPOINT_URL = 'https://%s' % AWS_S3_CUSTOM_DOMAIN
# AWS_QUERYSTRING_AUTH = False

MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
AWS_S3_ENDPOINT_URL = 'https://%s' % AWS_S3_HOST
