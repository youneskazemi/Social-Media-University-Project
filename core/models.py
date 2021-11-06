from django.db import models
from accounts.models import User as MyUser
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    image = models.ImageField(default='2.png', null=True, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[:30]

    class Meta:
        ordering = ('-updated',)
