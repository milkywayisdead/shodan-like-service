from django.contrib import admin

from content import models


admin.site.register(models.NewsArticle)
admin.site.register(models.Filter)
admin.site.register(models.Functionality)