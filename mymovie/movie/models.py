from django.db import models

# Create your models here.
from django.utils import timezone
# Create your models here.
# 地区
Region = (
    ('1', '中国大陆'),
    ('2', '美国'),
    ('3', '英国'),
    ('4', '法国'),
    ('5', '日本'),
    ('6', '韩国'),
    ('7', '其他'),
)
# 清晰度
Quality = (
    ('3', '720p'),
    ('4', '1080p'),
    ('5', '4k'),
)
# 热门
Hot = (
    ('1', '是'),
    ('2', '否'),
)
# 置顶
Top = (
    ('1', '是'),
    ('2', '否'),
)
# 免费
FREE = (
    ('1', '是'),
    ('2', '否'),
)
# 显示
Show = (
    ('1', '是'),
    ('2', '否'),
)
class Category(models.Model):
    Category_name = models.CharField(max_length=100, verbose_name='分类名称')
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = u'Category'
        verbose_name = '电影分类'
        verbose_name_plural = '分类管理'
    
    def __str__(self):
        return self.Category_name
class Movie(models.Model):
        # 电影信息
    id = models.AutoField(primary_key=True)
    Movie_name = models.CharField(max_length=100, verbose_name='电影名称')
    Movie_director = models.CharField(max_length=100, verbose_name='导演')
    scriptwriter = models.CharField(max_length=100, verbose_name='编剧')
    Movie_actor = models.CharField(max_length=100, verbose_name='演员')
    Movie_type = models.CharField(max_length=100, verbose_name='类型')
    Movie_length = models.IntegerField(verbose_name='片长')
    Movie_score = models.FloatField(verbose_name='评分')
    Movie_describe = models.TextField(verbose_name='电影简介', blank=True, null=True)
    Movie_image = models.ImageField(upload_to='movie_images', verbose_name='电影海报')
    Movie_language = models.CharField(max_length=100, verbose_name='语言')
    Movie_area = models.CharField(choices=Region,max_length=100, verbose_name='地区')
    Movie_release_date = models.DateField(verbose_name='上映日期', default=timezone.now)
    Movie_duration = models.CharField(max_length=100, verbose_name='时长')
    Movie_douban_score = models.CharField(max_length=100, verbose_name='豆瓣评分')
    Movie_subtitle = models.CharField(max_length=100, verbose_name='字幕')
    Movie_update_info = models.CharField(max_length=100, verbose_name='更新信息')
    Movie_Storage = models.TextField(max_length=200, verbose_name='网盘信息', default='', help_text='每个网盘信息占一行，每个字段用网盘名:网址 提取码:字符组成(无提取码不写)。如 百度网盘:http:/www.baidu.com 提取码:8888', null=True, blank=True)
    Movie_is_hot = models.CharField(choices=Hot, max_length=1, default='2', verbose_name='是否热门')
    Movie_is_top = models.CharField(choices=Top, max_length=1, default='2', verbose_name='是否置顶')
    Movie_is_free = models.CharField(choices=FREE, max_length=1, default='2', verbose_name='是否免费')
    Movie_is_show = models.CharField(choices=Show, max_length=1, default='1', verbose_name='是否显示')
    Movie_clear_rate = models.CharField(choices=Quality, max_length=1, default='1', verbose_name='清晰度')

    # 电影分类
    Movie_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='电影分类')
    class Meta:
        db_table = 'Movie'
        verbose_name = '电影信息'
        verbose_name_plural = '电影管理'
        ordering = ['Movie_name']  # 默认按电影名称排序

    def __str__(self):
        return self.Movie_name