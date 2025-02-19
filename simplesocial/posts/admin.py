from django.contrib import admin
from . import models

class PostInLine(admin.TabularInline):
    model = models.Post

admin.site.register(models.Post)
