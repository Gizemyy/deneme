from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone

class Spaces(models.Model):
    author = models.ForeignKey('auth.User', verbose_name="kurucu",on_delete=models.CASCADE, related_name='space')
    title = models.CharField(max_length=100, verbose_name="başlık")
    description = models.CharField(max_length=500, verbose_name="açıklama", null=True, blank=True)
    slug = models.SlugField(max_length=130, unique=True, editable=False)
    followers = models.ManyToManyField(User, related_name="followers", blank=True)
    profile_pic = models.ImageField(upload_to='space_pictures', blank=True, verbose_name='profilepic',default='default.jpg')

    @property
    def image_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url


    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('ask:home')

    def get_unique_slug(self):
        slug = slugify(self.title.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while Spaces.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Spaces, self).save(*args, **kwargs)

