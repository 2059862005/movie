from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from djoser.serializers import UserSerializer

from account.models import ProFile
class CustomUniqueValidator(UniqueValidator):
    def __call__(self, value, serializer_field):
        self.message = _('邮箱 %s 已被注册') % value
        return super().__call__(value, serializer_field)    

class CustomUserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(
        validators=[ CustomUniqueValidator(queryset=User.objects.all())]
    )
    def create(self, validated_data):
        user = UserCreateSerializer.create(self, validated_data)
        # 写入到ProFile表   
        proFile = ProFile(user=user, email=user.email)
        proFile.save()
        return user

    class Meta:
        model = User
        fields = ('id','username', 'email', 'password')

class profilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProFile
        fields = '__all__'

class CustomUserSerializer(UserSerializer):
    profile = profilleSerializer(read_only=True)
    class Meta:
        model = User
        fields = (*UserSerializer.Meta.fields, 'profile')
    pass

