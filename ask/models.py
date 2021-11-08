from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from spaces.models import Spaces
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Question(models.Model):
    user = models.ForeignKey('auth.User', verbose_name="yazar", on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=120, verbose_name="Soru")
    publishing_date = models.DateTimeField(verbose_name="Yayınlanma tarihi", default=timezone.now)
    slug = models.SlugField(max_length=130, unique=True, editable=False)
    picture = CloudinaryField('image')
    upvoters = models.ManyToManyField(User, related_name="upvoters", blank=True)
    downvoters = models.ManyToManyField(User, related_name="downvoters", blank=True)


    def __str__(self):
        return self.question


    def get_absolute_url(self):
        return reverse('ask:home')

    def get_unique_slug(self):
        slug = slugify(self.question.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while Question.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Question, self).save(*args, **kwargs)





class Comment(models.Model):
    question = models.ForeignKey(Question, related_name='comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=300, verbose_name="yorum")
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=100, verbose_name="user")

    def __str__(self):
        return self.content

class SpaceQuestion(models.Model):
    user = models.ForeignKey('auth.User', verbose_name="Yazar", on_delete=models.CASCADE, related_name='spacequestions')
    question = models.CharField(max_length=500, verbose_name="Soru")
    publishing_date = models.DateTimeField(verbose_name="Yayınlanma tarihi", default=timezone.now)
    slug = models.SlugField(max_length=130, unique=True, editable=False)
    category = models.ForeignKey(Spaces, on_delete=models.CASCADE, related_name="category")
    picture = models.ImageField(upload_to='question_pictures', blank=True)
    upvoters = models.ManyToManyField(User, related_name="upvoterssq", blank=True)
    downvoters = models.ManyToManyField(User, related_name="downvoterssq", blank=True)

    def __str__(self):
        return self.question

    def get_unique_slug(self):
        slug = slugify(self.question.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while SpaceQuestion.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(SpaceQuestion, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ask:home')

class SpaceQuestionComment(models.Model):
    question = models.ForeignKey(SpaceQuestion, related_name='spacecomments', on_delete=models.CASCADE)
    content = models.CharField(max_length=300, verbose_name="sqyorum")
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=100, verbose_name="user")

    def __str__(self):
        return self.content



