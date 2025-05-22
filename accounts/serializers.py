from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password         = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'phone', 'birth_date', 'role', 'password', 'confirm_password'
        ]

    @staticmethod
    def validate_username(value):
        if CustomUser.objects.filter(username=value.lower()).exists():
            raise serializers.ValidationError("Ya existe un usuario con ese nombre de usuario.")
        return value.lower()

    @staticmethod
    def validate_email(value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe un usuario con ese correo.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(
            password=password,
            **validated_data
        )
        return user


# serializers.py
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role  # 👈 esto es lo importante
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role  # 👈 esto devuelve el rol en la respuesta
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'birth_date', 'role', 'date_joined']
        read_only_fields = ['username', 'email', 'role', 'date_joined']  # ❗️ Estos campos NO se podrán editar

