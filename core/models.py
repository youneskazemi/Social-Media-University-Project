from django.db import models

from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
