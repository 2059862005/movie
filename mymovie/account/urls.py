from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .models import account
from views import ProFileViewSet
"""
URL配置 通过 framework.routers.DefaultRouter() 来自动生成URL路由        
"""
# 初始化路由器
router = DefaultRouter()

# 注册视图集到路由器
router.register(r'movies', ProFileViewSet, basename='movie')
