from django.db import models
from uuid import uuid4
from rest_framework import serializers


def upload_image(instance, filename):
    return f'{instance.id}-{filename}'

class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=upload_image, blank=True, null=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=False)
    category = models.CharField(max_length=100, blank=True, null=False)
    title = models.CharField(max_length=100, blank=True, null=False)
    summary = models.CharField(max_length=200, blank=True, null=False)
    firstParagraph = models.CharField(max_length=100, blank=True, null=False)
    body = models.CharField(max_length=9000, blank=True, null=False)

    def clean(self):
        if len(self.body) < 50:
            raise serializers.ValidationError({'body': 'body need to have at least 50 digits'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
