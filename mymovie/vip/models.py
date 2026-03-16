from django.db import models
from django.utils import timezone
# Create your models here.

class vip(models.Model):
    card_name = models.CharField("会员卡名称", max_length=100, unique=True)
    card_price = models.DecimalField("价格", max_digits=8, decimal_places=2)
    duration = models.IntegerField("有效天数")
    info = models.CharField("会员卡简介", max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="更新时间")

    class Meta:
        db_table = 'card'
        verbose_name = "会员卡信息"
        verbose_name_plural = verbose_name
        ordering = ['created_at']
