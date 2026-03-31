# 第一个开发的网站
## 项目概述

这是一个 Django + (DRF) 开发的电影网站，这是我第一个开发的完整网站 其中有很多bug 还有定单系统没有开发完成 

---

## 一、模型关系 (Models)

### 1.1 核心模型架构

```
User (Django内置)  ──────<OneToOne>──────>  ProFile (自定义用户资料)
                                              │
                                              └────────<ManyToMany>────────> Movie
```

### 1.2 ProFile 模型 (account/models.py)

```python
class ProFile(models.Model):
    # 基本信息
    uid              # ShortUUIDField - 用户唯一ID
    phone            # CharField - 手机号
    email            # EmailField - 邮箱
    avatar           # ImageField - 头像
    
    # VIP会员相关
    is_upgrade       # BooleanField - 是否升级会员
    upgrade_time     # DateTimeField - 升级时间
    expire_time      # DateTimeField - 过期时间
    upgrade_count    # CharField - 升级次数
    
    # ====== 核心关系字段 ======
    
    # 1. 与Django User的一对一关系
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # 2. 与Movie的多对多关系 (4种收藏状态)
    movie_collection = models.ManyToManyField(Movie, related_name='movie_collection')  # 收藏
    movie_wish       = models.ManyToManyField(Movie, related_name='movie_wish')         # 想看
    movie_do         = models.ManyToManyField(Movie, related_name='movie_do')          # 在看
    movie_collect    = models.ManyToManyField(Movie, related_name='movie_collect')      # 看过
    
    # 另一个收藏关系 (备用)
    movies = models.ManyToManyField(Movie)
```

### 1.3 Movie 模型 (movie/models.py)

```python
class Movie(models.Model):
    # 电影基本信息
    Movie_name         # 电影名称
    Movie_director    # 导演
    scriptwriter      # 编剧
    Movie_actor       # 演员
    Movie_type        # 类型
    Movie_length      # 片长
    Movie_score       # 评分
    Movie_describe    # 简介
    Movie_image       # 海报
    
    # 关联分类
    Movie_category = models.ForeignKey(Category, on_delete=models.CASCADE)
```

---

## 二、序列化器关系 (Serializers)

### 2.1 序列化器层级

```
CustomUserCreateSerializer
    │
    ├── 继承自: UserCreateSerializer (Djoser)
    │
    └── 功能: 
        ├── 验证email唯一性
        └── create()时同时创建ProFile记录
        (用户注册 → 自动创建用户资料)

profilleSerializer (ModelSerializer)
    │
    ├── 序列化: ProFile模型所有字段
    │
    └── 用途: 嵌套在CustomUserSerializer中

CustomUserSerializer
    │
    ├── 继承自: UserSerializer (Djoser)
    │
    ├── 嵌套: profilleSerializer (read_only=True)
    │
    └── 效果: 返回用户信息时同时返回用户资料
```

### 2.2 代码对应关系

| Serializer | 关联Model | 用途 |
|-----------|----------|------|
| `CustomUserCreateSerializer` | User | 用户注册 |
| `profilleSerializer` | ProFile | 用户资料序列化 |
| `CustomUserSerializer` | User + ProFile | 获取用户信息(含资料) |

---

## 三、视图关系 (Views)

### 3.1 CollectViewSet - 电影收藏视图集

```python
class CollectViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
```

**API端点与功能对应：**

| 方法 | 路径 | 功能 | 说明 |
|-----|------|------|------|
| `GET` | `/api/collects/` | 列出收藏 | 返回当前用户收藏的所有电影 |
| `POST` | `/api/collects/` | 添加收藏 | 需提供 `movie_id` 参数 |
| `DELETE` | `/api/collects/{pk}/` | 取消收藏 | 根据电影ID删除 |
| `GET` | `/api/collects/{pk}/is_collected/` | 检查收藏状态 | 自定义action |

### 3.2 视图工作流程

```
请求 → CollectViewSet
    │
    ├── list() ─────────> 获取profile.movies.all() ──> MovieSerializer ──> JSON
    │
    ├── create() ──────> 获取profile ──> profile.movies.add(movie) ──> 成功/失败
    │
    ├── destroy() ─────> 获取profile ──> profile.movies.remove(movie) ──> 成功/失败
    │
    └── is_collected() ─> 检查profile.movies中是否存在该电影 ──> Boolean
```

---

## 四、数据流关系图

### 4.1 用户注册流程

```
POST /api/users/
    │
    ▼
CustomUserCreateSerializer
    │
    ├── 验证email唯一性
    ├── 创建User对象
    │
    └── create():
        ├── user = User.objects.create_user()
        ├── profile = ProFile.objects.create(user=user, email=user.email)
        │
        └── return user
```

### 4.2 收藏操作流程

```
POST /api/collects/  (body: {"movie_id": 1})
    │
    ▼
CollectViewSet.create()
    │
    ├── request.user ──> ProFile.objects.get(user=user)
    ├── movie_id ──> Movie.objects.get(id=movie_id)
    │
    └── profile.movies.add(movie)
        │
        └── 保存到数据库 (多对多关系表)
```

### 4.3 获取用户信息流程

```
GET /api/users/me/  (需要JWT token)
    │
    ▼
CustomUserSerializer (Djoser内置)
    │
    ├── 返回User字段: id, username, email
    │
    └── 嵌套 profilleSerializer:
        ├── avatar
        ├── phone
        ├── is_upgrade
        ├── movie_collection (ManyToMany)
        └── ...其他ProFile字段
```

---

## 五、URL路由汇总

### 5.1 主路由 (ssy_movie/urls.py)

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('movie.urls')),        # 电影API
    path('api/', include('djoser.urls')),        # 用户认证(注册/登录)
    path('api/', include('djoser.urls.jwt')),   # JWT token
    path('api/', include(router.urls)),         # 收藏API
    path('api/collects/', ...),                 # 收藏端点
    path('api/alipay/', ...),                   # 支付
]
```

### 5.2 Account应用路由 (account/urls.py)

```python
urlpatterns = [
    path('verify/', VerifyTokenView.as_view()),  # Token验证
]
```

---

## 六、关键字段关系速查表

### ProFile 中的多对多关系

| 字段名 | related_name | 用途 | Django ORM |
|-------|-------------|------|------------|
| `movie_collection` | `movie_collection` | 收藏的电影 | `profile.movie_collection.all()` |
| `movie_wish` | `movie_wish` | 想看的电影 | `profile.movie_wish.all()` |
| `movie_do` | `movie_do` | 在看的电影 | `profile.movie_do.all()` |
| `movie_collect` | `movie_collect` | 看过的电影 | `profile.movie_collect.all()` |
| `movies` | (默认) | 备用收藏 | `profile.movies.all()` |

---

## 七、技术栈

- **Django** - Web框架
- **Django REST Framework** - REST API
- **Djoser** - 用户认证(注册/登录/JWT)
- **ShortUUIDField** - 短UUID生成

---

