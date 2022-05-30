from django.contrib import admin
from .models import (
    Endpoint,
    MLAlgorithm,
    MLRequest,
    EnglishToHindiTranslation,
    myuploadfile,
    review,
    myuploadgujaratifile,
)

# Register your models here.
admin.site.register(Endpoint)
admin.site.register(MLAlgorithm)
admin.site.register(MLRequest)
admin.site.register(myuploadfile)
admin.site.register(myuploadgujaratifile)
admin.site.register(review)


class AdminEnglishHindi(admin.ModelAdmin):
    search_fields = ("english",)


admin.site.register(EnglishToHindiTranslation, AdminEnglishHindi)











