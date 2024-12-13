from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',  'password', 'email', 'phone_number')

    extra_kwargs = {
        'username': {'required': True, 'allow_blank': False},
        'password': {'required': True, 'allow_blank': False},
        'email': {'required': False, 'allow_blank': True},
        'phone_number': {'required': False, 'allow_blank': True},
    }


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',  'password')


class UserRetrieveSerializer(serializers.ModelSerializer):
    mentor = serializers.StringRelatedField()
    students = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'phone_number', 'mentor', 'students', 'password')


class UserListSerializer(serializers.ModelSerializer):
    mentor = serializers.StringRelatedField()
    students = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'mentor', 'students')


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenBlacklistRequestSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
