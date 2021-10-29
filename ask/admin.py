from django.contrib import admin

# Register your models here.
from ask.models import Question,SpaceQuestion,Comment,SpaceQuestionComment

admin.site.register(Question)
admin.site.register(SpaceQuestion)
admin.site.register(Comment)
admin.site.register(SpaceQuestionComment)

