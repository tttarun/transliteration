from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EndpointView,
    MLAlgoirthmView,
    MLRequestView,
    TranslateView,
    SearchAndUpdateAPIView,
    TranslateStringView,
    Home,
    ExcelFileTranslate,
    send_files,
    reviewandcomment,
    Gujarati,
    Hindi,
    TranslateGujaratiStringView,
    send_files_gujarati,
    UpdateHindiScoreAPIView,
    UpdateGujaratiScoreAPIView,
)
from rest_framework import routers
from . import views

router = DefaultRouter()
router.register(r"endpoints", EndpointView, basename="endpoints")
router.register(r"mlalgorithms", MLAlgoirthmView, basename="mlalgorithms")
router.register(r"mlrequest", MLRequestView, basename="mlrequest")


urlpatterns = [
    path("", Home.as_view(), name="Home"),
    path("v1/", include(router.urls)),
    path("v1/translate/<str:endpoint>/", TranslateView.as_view(), name="translate"),
    path("v1/translate", TranslateStringView.as_view(), name="translatestring"),
    path("v1/translate_gujarati", TranslateGujaratiStringView.as_view(), name="translategujaratistring"),
    path("v1/translation/update", SearchAndUpdateAPIView.as_view()),
    path("v1/exceltranslate/", ExcelFileTranslate.as_view()),
    path("upload", send_files.as_view(), name="uploads"),
    path("review", reviewandcomment.as_view(),name="review"),
    path("gujarati", Gujarati.as_view(), name="gujarati"),
    path("hindi", Hindi.as_view(), name="hindi"),
    path("uploadgujarati", send_files_gujarati.as_view(), name="uploadsgujarati"),
    path("uploadhindiscore", UpdateHindiScoreAPIView.as_view(), name="uploadhindiscore"),
    path("uploadgujaratiscore", UpdateGujaratiScoreAPIView.as_view(), name="uploadgujaratiscore"),
]
