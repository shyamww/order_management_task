from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.api.views import OrderViewSet, MetricsViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'metrics', MetricsViewSet, basename='metrics')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]