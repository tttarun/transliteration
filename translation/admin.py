from django.contrib import admin
from .models import (
    Endpoint,
    MLAlgorithm,
    MLRequest,
    EnglishToHindiTranslation,
    myuploadfile,
)

# Register your models here.
admin.site.register(Endpoint)
admin.site.register(MLAlgorithm)
admin.site.register(MLRequest)
admin.site.register(myuploadfile)


class AdminEnglishHindi(admin.ModelAdmin):
    search_fields = ("english",)


admin.site.register(EnglishToHindiTranslation, AdminEnglishHindi)
