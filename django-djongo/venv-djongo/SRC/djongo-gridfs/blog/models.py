#from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from djongo import models
from djongo.storage import GridFSStorage

gridfs_storage = GridFSStorage(collection='images',
                               base_url=''.join([settings.BASE_DIR, 'images/']))


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    avatar = models.ImageField(upload_to='authors',
                               storage=gridfs_storage)

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    rating = models.IntegerField()
    featured_image = models.ImageField(upload_to='entries',
                                       storage=gridfs_storage)

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse('detail', args=(str(self.pk)))

    def save(self, *args, **kwargs):
        """ on save, update timestamps, instead of auto_now field args """
        if not self.pk:
            self.pub_date = timezone.now()
        self.mod_date = timezone.now()
        return super().save(*args, **kwargs)
