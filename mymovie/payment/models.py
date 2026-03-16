from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('failed', '支付失败'),
        ('refunded', '已退款'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    out_trade_no = models.CharField(max_length=64, unique=True, verbose_name='商户订单号')
    trade_no = models.CharField(max_length=64, blank=True, verbose_name='支付宝交易号')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额')
    subject = models.CharField(max_length=200, verbose_name='商品标题')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    vip_card_id = models.IntegerField(verbose_name='VIP卡ID')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')

    class Meta:
        db_table = 'payment'
        verbose_name = '支付记录'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
