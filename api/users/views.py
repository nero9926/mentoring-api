from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.permissions import IsAuthorOrReadOnlyPermission
from users.serializers import (
    TokenBlacklistRequestSerializer,
    TokenObtainPairResponseSerializer,
    UserListSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserRetrieveSerializer,
)

User = get_user_model()


class UserViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet):
    """Вьюсет для работы с пользователями"""
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_serializer_class(self):
        user = self.request.user
        pk = self.kwargs.get('pk')

        if user.is_authenticated and str(user.pk) == pk:
            return UserRetrieveSerializer
        return super().get_serializer_class()

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        mentor_name = data.get('mentor', None)
        if mentor_name is not None:
            try:
                mentor = User.objects.get(username=mentor_name)
                user = self.request.user
                user.mentor = mentor
                user.save()
            except Exception:
                raise APIException(
                    detail='Пользователь с указанным именем отсутствует',
                    code=400)
        return super().partial_update(request, *args, **kwargs)


class RegistrationAPIView(APIView):
    """Кастомное представление для регистрации пользователей"""
    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        }
    )
    def post(self, request: Request) -> Response:
        data = request.data
        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            user = User.objects.create(
                username=serializer.validated_data.get('username', None),
                password=serializer.validated_data.get('password', None),
                email=serializer.validated_data.get('email', None),
                phone_number=serializer.validated_data.get(
                    'phone_number', None),
            )
            user.save()
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({
                'user_id': user.id,
                'username': user.username
            })
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class LoginAPIView(APIView):
    """Кастомное представление для авторизации пользователей"""
    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        }
    )
    def post(self, request: Request) -> Response:
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None or password is None:
            return Response({'error': 'Нужен и логин, и пароль'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(
                username=data['username'], password=data['password'])
        except Exception:
            raise APIException(detail='Неверно указаны данные', code=400)

        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'username': user.username
        })
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    """Кастомное представление для выхода пользователей"""
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=TokenBlacklistRequestSerializer,
    )
    def post(self, request: Request) -> Response:
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Необходим Refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({'error': 'Неверный Refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'Успешно'},
                        status=status.HTTP_200_OK)
