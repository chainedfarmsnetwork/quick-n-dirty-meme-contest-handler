from django.contrib import admin

from .models import MemeContest, MemeContestPost, RetweetPost

admin.site.register(MemeContest)
admin.site.register(MemeContestPost)
admin.site.register(RetweetPost)
