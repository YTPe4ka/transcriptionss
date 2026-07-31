from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer, UserProfileSerializer
from drf_spectacular.utils import extend_schema

User = get_user_model()

# Эндпоинт регистрации нового пользователя (доступен публично без токена)
@extend_schema(summary="Foydalanuvchini roʻyxatdan oʻtkazish", tags=["Auth"])
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)

# Эндпоинт получения и редактирования профиля текущего пользователя (требует JWT авторизацию)
@extend_schema(summary="Foydalanuvchi profil ma'lumotlari", tags=["Auth"])
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # Метод возвращает объект текущего авторизованного пользователя из JWT токена
    def get_object(self):
        return self.request.user
