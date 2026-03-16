from rest_framework import serializers
from movie.models import Movie, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'Category_name']

class MovieListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='Movie_category.Category_name', read_only=True)
    region_display = serializers.CharField(source='get_Movie_area_display', read_only=True)
    quality_display = serializers.CharField(source='get_Movie_clear_rate_display', read_only=True)
    
    class Meta:
        model = Movie
        fields = [
            'id', 'Movie_name', 'Movie_image', 'Movie_score', 
            'Movie_type', 'Movie_area', 'region_display',
            'Movie_category', 'category_name', 'Movie_clear_rate', 
            'quality_display', 'Movie_is_hot', 'Movie_is_top', 
            'Movie_is_free', 'Movie_is_show', 'Movie_douban_score'
        ]

class MovieDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='Movie_category.Category_name', read_only=True)
    region_display = serializers.CharField(source='get_Movie_area_display', read_only=True)
    quality_display = serializers.CharField(source='get_Movie_clear_rate_display', read_only=True)
    
    class Meta:
        model = Movie
        fields = '__all__'

class MovieCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'Movie_name', 'Movie_director', 'scriptwriter', 'Movie_actor',
            'Movie_type', 'Movie_length', 'Movie_score', 'Movie_describe',
            'Movie_image', 'Movie_language', 'Movie_area', 'Movie_release_date',
            'Movie_duration', 'Movie_douban_score', 'Movie_subtitle',
            'Movie_update_info', 'Movie_Storage', 'Movie_is_hot', 'Movie_is_top',
            'Movie_is_free', 'Movie_is_show', 'Movie_clear_rate', 'Movie_category'
        ]
