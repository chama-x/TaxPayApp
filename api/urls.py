from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'assessment-tax', views.AssessmentTaxViewSet)
router.register(r'business-tax', views.BusinessTaxViewSet)
router.register(r'industrial-tax', views.IndustrialTaxViewSet)
router.register(r'trade-license', views.TradeLicenseViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'documents', views.DocumentViewSet)
router.register(r'notifications', views.NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 