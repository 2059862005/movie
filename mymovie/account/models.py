from django.db import models
from movie.models import Movie
from django.contrib.auth.models import User
class ProFile(models.Model):
    uid = models.CharField(max_length=32, primary_key=True,unique=True,verbose_name='用户ID',db_index=True)
    phone = models.CharField(max_length=11, null=True, blank=True,verbose_name='手机号',db_index=True)
    email = models.EmailField(null=True,blank=True,verbose_name='邮箱',db_index=True)
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True,verbose_name='头像')
    # vip
    is_upgrade = models.BooleanField(default=False,verbose_name='是否升级会员')
    upgrade_time = models.DateTimeField(null=True, blank=True,verbose_name='升级时间')
    expire_time = models.DateTimeField(null=True, blank=True,verbose_name='过期时间')
    upgrade_count = models.IntegerField(default=0,verbose_name='升级次数')
    # 
    movie_collection = models.ManyToManyField(Movie, related_name='movie_collection',verbose_name='电影收藏')
    movie_wish = models.ManyToManyField(Movie, related_name='movie_wish',verbose_name='想看的电影')
    movie_do = models.ManyToManyField(Movie, related_name='movie_do',verbose_name='在看的电影')
    movie_collect = models.ManyToManyField(Movie, related_name='movie_collect',verbose_name='看过的电影')
    # 关联用户
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name='用户') 
    # 关联电影表
    movies = models.ManyToManyField(Movie, related_name='profile_movies')
    class Meta:
        db_table = 'ProFile'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
