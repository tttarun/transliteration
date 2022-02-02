from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import EndpointView, MLAlgoirthmView, MLRequestView, TranslateView, translateAPIView, SearchAndUpdateAPIView

router = DefaultRouter()
router.register(r'endpoints', EndpointView, basename='endpoints')
router.register(r'mlalgorithms',MLAlgoirthmView, basename='mlalgorithms')
router.register(r'mlrequest', MLRequestView, basename='mlrequest')
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/<str:endpoint>/', TranslateView.as_view(),name='translate'),
    path('', include(router.urls)),
    path('translate/<str:given_string>', translateAPIView.as_view()),
    path('translation/update', SearchAndUpdateAPIView.as_view()),

]
