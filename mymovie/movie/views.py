from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from movie.models import Movie, Category
from movie.serializers import (
    CategorySerializer, MovieListSerializer, 
    MovieDetailSerializer, MovieCreateUpdateSerializer
)
from account.models import ProFile

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    search_fields = ['Category_name']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['Movie_category', 'Movie_area', 'Movie_is_hot', 'Movie_is_top', 'Movie_is_free', 'Movie_is_show', 'Movie_clear_rate']
    search_fields = ['Movie_name', 'Movie_actor', 'Movie_director', 'Movie_type']
    ordering_fields = ['Movie_score', 'Movie_release_date', 'Movie_name']
    ordering = ['-Movie_is_top', '-Movie_score']

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MovieCreateUpdateSerializer
        return MovieDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(Movie_is_show='1')
        return queryset

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def play(self, request, pk=None):
        movie = self.get_object()
        profile = request.user.profile
        if movie.Movie_is_free == '2' and not profile.is_upgrade:
            return Response({'error': 'VIP会员才能观看'}, status=status.HTTP_403_FORBIDDEN)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def collect(self, request, pk=None):
        movie = self.get_object()
        profile = request.user.profile
        if movie in profile.movie_collection.all():
            profile.movie_collection.remove(movie)
            return Response({'status': '取消收藏成功'})
        profile.movie_collection.add(movie)
        return Response({'status': '收藏成功'})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def wish(self, request, pk=None):
        movie = self.get_object()
        profile = request.user.profile
        if movie in profile.movie_wish.all():
            profile.movie_wish.remove(movie)
            return Response({'status': '取消想看成功'})
        profile.movie_wish.add(movie)
        return Response({'status': '想看成功'})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def watching(self, request, pk=None):
        movie = self.get_object()
        profile = request.user.profile
        if movie in profile.movie_do.all():
            profile.movie_do.remove(movie)
        profile.movie_do.add(movie)
        return Response({'status': '添加到在看成功'})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def watched(self, request, pk=None):
        movie = self.get_object()
        profile = request.user.profile
        if movie in profile.movie_do.all():
            profile.movie_do.remove(movie)
        profile.movie_collect.add(movie)
        return Response({'status': '添加到看过成功'})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_collections(self, request):
        profile = request.user.profile
        movies = profile.movie_collection.all()
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_wishes(self, request):
        profile = request.user.profile
        movies = profile.movie_wish.all()
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_watching(self, request):
        profile = request.user.profile
        movies = profile.movie_do.all()
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_watched(self, request):
        profile = request.user.profile
        movies = profile.movie_collect.all()
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)
