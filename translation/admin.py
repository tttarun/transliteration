from django.contrib import admin
from .models import Endpoint, MLAlgorithm, MLRequest, EnglishToHindiTranslation

# Register your models here.
admin.site.register(Endpoint)
admin.site.register(MLAlgorithm)
admin.site.register(MLRequest)


class AdminEnglishHindi(admin.ModelAdmin):
    search_fields = ('english',)


admin.site.register(EnglishToHindiTranslation, AdminEnglishHindi)
