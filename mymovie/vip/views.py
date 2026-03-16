from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.utils import timezone
from datetime import timedelta
from vip.models import vip
from vip.serializers import VipCardSerializer

class VipCardViewSet(viewsets.ModelViewSet):
    queryset = vip.objects.all()
    serializer_class = VipCardSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

class VipViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_vip(self, request):
        profile = request.user.profile
        return Response({
            'is_upgrade': profile.is_upgrade,
            'upgrade_time': profile.upgrade_time,
            'expire_time': profile.expire_time,
            'upgrade_count': profile.upgrade_count,
        })

    @action(detail=True, methods=['post'])
    def buy(self, request, pk=None):
        try:
            card = vip.objects.get(pk=pk)
        except vip.DoesNotExist:
            return Response({'error': 'VIP卡不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        profile = request.user.profile
        now = timezone.now()
        
        if profile.is_upgrade and profile.expire_time and profile.expire_time > now:
            new_expire_time = profile.expire_time + timedelta(days=card.duration)
        else:
            new_expire_time = now + timedelta(days=card.duration)
        
        profile.is_upgrade = True
        profile.upgrade_time = now
        profile.expire_time = new_expire_time
        profile.upgrade_count += 1
        profile.save()
        
        return Response({
            'status': '开通成功',
            'expire_time': new_expire_time,
            'card_name': card.card_name
        })
