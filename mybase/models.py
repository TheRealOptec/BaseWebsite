from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

import datetime

class Topic(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=500, unique=False, default="")
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Topic, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Page(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    body = models.CharField(max_length=500, default="")
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Page, on_delete=models.CASCADE)
    body = models.CharField(max_length=320)
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Got datetime stuff from: https://stackoverflow.com/questions/415511/how-do-i-get-the-current-time-in-python
        self.created_at = datetime.datetime.now()
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return self.body

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pfp = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.user.username