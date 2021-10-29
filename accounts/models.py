
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from spaces.models import Spaces
from ask.models import Question, SpaceQuestion

class Profile(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]

    user = models.ForeignKey(User, related_name="profile", on_delete=models.CASCADE)
    following = models.ManyToManyField(Spaces, related_name="following", blank=True)
    profile_pic = models.ImageField(upload_to="profiles", null=True, blank=True, default='default.jpg')
    birthday = models.DateField(null=True, blank=True, verbose_name="birthday")
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    following_user = models.ManyToManyField(User, related_name="following_user", blank=True)
    follower_user = models.ManyToManyField(User, related_name="follower_user",  blank=True)
    upvoting = models.ManyToManyField(Question, related_name="upvoting", blank=True)
    downvoting = models.ManyToManyField(Question, related_name="downvoting", blank=True)
    upvotingsq = models.ManyToManyField(SpaceQuestion, related_name="upvotingsq", blank=True)
    downvotingsq = models.ManyToManyField(SpaceQuestion, related_name="downvotingsq", blank=True)


    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('accounts:profile')


    @property
    def image_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url