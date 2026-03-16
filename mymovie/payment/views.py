from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
import uuid
from payment.models import Payment
from payment.serializers import PaymentSerializer
from vip.models import vip
from utils.payment import Alipay
from account.models import ProFile

class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_order(self, request):
        vip_card_id = request.data.get('vip_card_id')
        try:
            card = vip.objects.get(pk=vip_card_id)
        except vip.DoesNotExist:
            return Response({'error': 'VIP卡不存在'}, status=status.HTTP_404_NOT_FOUND)
        
        out_trade_no = f"{timezone.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8]}"
        
        payment = Payment.objects.create(
            user=request.user,
            out_trade_no=out_trade_no,
            amount=card.card_price,
            subject=f'{card.card_name} - VIP会员',
            vip_card_id=card.id,
        )
        
        alipay = Alipay()
        pay_url = alipay.build_url(out_trade_no, payment.subject, float(card.card_price))
        
        return Response({
            'order_id': out_trade_no,
            'pay_url': pay_url,
            'amount': card.card_price
        })

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        payments = Payment.objects.filter(user=request.user)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def check_order(self, request):
        out_trade_no = request.query_params.get('out_trade_no')
        try:
            payment = Payment.objects.get(out_trade_no=out_trade_no, user=request.user)
            return Response({
                'status': payment.status,
                'amount': payment.amount,
                'paid_at': payment.paid_at
            })
        except Payment.DoesNotExist:
            return Response({'error': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def alipay_notify(self, request):
        alipay = Alipay()
        params = request.data.dict()
        
        if not alipay.verify(params):
            return Response({'status': 'fail'})
        
        out_trade_no = params.get('out_trade_no')
        trade_no = params.get('trade_no')
        trade_status = params.get('trade_status')
        
        try:
            payment = Payment.objects.get(out_trade_no=out_trade_no)
        except Payment.DoesNotExist:
            return Response({'status': 'success'})
        
        if trade_status in ['TRADE_SUCCESS', 'TRADE_FINISHED']:
            payment.status = 'paid'
            payment.trade_no = trade_no
            payment.paid_at = timezone.now()
            payment.save()
            
            card = vip.objects.get(id=payment.vip_card_id)
            profile = payment.user.profile
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
        
        return Response({'status': 'success'})
