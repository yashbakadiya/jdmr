from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Tag(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=127)
    content = CKEditor5Field(
                      config_name='default',
                      null=True,
                      blank=True
                  )
    author = models.CharField(max_length=63)
    timestamp = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to="blog/thumbnails")
    publish = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(null=True, blank=True, unique=True)
    tag = models.ManyToManyField(Tag, blank=True)


    class Meta:
        ordering = ['-timestamp']

    def __str__(self) -> str:
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.CharField(max_length=63)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()


class SubComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.CharField(max_length=63)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
