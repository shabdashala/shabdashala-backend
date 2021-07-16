from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage

# References:
# https://www.section.io/engineering-education/how-to-upload-files-to-aws-s3-using-django-rest-framework/
# https://simpleisbetterthancomplex.com/tutorial/2017/08/01/how-to-setup-amazon-s3-in-a-django-project.html
# https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/


class StaticStorage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION
    default_acl = 'public-read'


class MediaStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    default_acl = 'public-read'


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False
