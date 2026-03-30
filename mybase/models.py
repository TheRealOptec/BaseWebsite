from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

class Topic(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=500, unique=False, default="")
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.created_at is None:
            self.created_at = timezone.now()
        super(Topic, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Page(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    body = models.CharField(max_length=500, default="")
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=False)

    created_at = models.DateTimeField()

    def _build_unique_slug(self):
        base_slug = slugify(self.title) or "post"
        slug = base_slug
        suffix = 2

        conflicting_posts = Page.objects.filter(topic=self.topic)
        if self.pk is not None:
            conflicting_posts = conflicting_posts.exclude(pk=self.pk)

        while conflicting_posts.filter(slug=slug).exists():
            slug = f"{base_slug}-{suffix}"
            suffix += 1

        return slug

    def save(self, *args, **kwargs):
        self.slug = self._build_unique_slug()
        if self.created_at is None:
            self.created_at = timezone.now()
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pfp = models.ImageField(upload_to='profile_image', blank=True)
    bio = models.CharField(max_length=500, default="")
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
    
class PostHistory(models.Model):
    post = models.ForeignKey(Page, on_delete=models.CASCADE)
    access_time = models.DateTimeField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.access_time = timezone.now()
        super(PostHistory, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} History: {self.post} - accessed on {self.access_time}"


class TopicHistory(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    access_time = models.DateTimeField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.access_time = timezone.now()
        super(TopicHistory, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} History: {self.topic} - accessed on {self.access_time}"
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Page, on_delete=models.CASCADE)
    body = models.CharField(max_length=320)
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Got datetime stuff from: https://stackoverflow.com/questions/415511/how-do-i-get-the-current-time-in-python
        if self.created_at is None:
            self.created_at = timezone.now()
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return self.body

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='post_likes')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topics_likes')

    class Meta:
        unique_together = ('user', 'post')

    def save(self, *args, **kwargs):
        self.post.likes += 1
        self.post.save()
        self.topic.likes += 1
        self.topic.save()
        super(PostLike, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.post.likes -= 1
        self.post.save()
        self.topic.likes -= 1
        self.topic.save()
        super(PostLike, self).delete(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} likes {self.post.title} on topic {self.topic.name}"
