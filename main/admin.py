from django.contrib import admin
from .models import *

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Answer)
admin.site.register(AnswerDetail)

