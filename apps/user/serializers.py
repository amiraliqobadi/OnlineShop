from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.user.models import Cart
from apps.user.models import User


class CartSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cart
		fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
	
	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'password', 'user_image',)
		read_only_fields = ('id', 'date_joined')
