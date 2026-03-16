from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vip.views import VipCardViewSet, VipViewSet

router = DefaultRouter()
router.register(r'cards', VipCardViewSet, basename='vip-card')

urlpatterns = [
    path('', include(router.urls)),
    path('my-vip/', VipViewSet.as_view({'get': 'my_vip'}), name='my-vip'),
    path('buy-vip/<int:pk>/', VipViewSet.as_view({'post': 'buy'}), name='buy-vip'),
]
