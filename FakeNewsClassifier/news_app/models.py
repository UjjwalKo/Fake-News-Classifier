from django.db import models
from django.contrib.postgres.fields import ArrayField

class Article(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    url = models.URLField()
    url_to_image = models.URLField(null=True, blank=True)
    published_at = models.DateTimeField()
    source_name = models.CharField(max_length=255)
    embedding = ArrayField(models.FloatField(), null=True, blank=True)
    language = models.CharField(max_length=10, default='en')

    def __str__(self):
        return self.title