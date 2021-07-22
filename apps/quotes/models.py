import uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel


class Quote(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    language = models.ForeignKey('languages.Language', on_delete=models.CASCADE)
    categories = models.ManyToManyField('categories.Category', blank=True)
    text = models.ForeignKey('sentences.Sentence', on_delete=models.CASCADE)
    credits = models.CharField(max_length=64, null=True, blank=True)
    description = models.CharField(max_length=512, null=True, blank=True)
    image = models.ImageField(max_length=256, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.text
