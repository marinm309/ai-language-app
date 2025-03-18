from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = '__all__'
	def create(self, clean_data):
		user_obj = UserModel.objects.create_user(email=clean_data['email'], name=clean_data['name'], password=clean_data['password'], image=clean_data['image'])
		user_obj.save()
		return user_obj

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	
	def check_user(self, clean_data):
		user = authenticate(email=clean_data['email'], password=clean_data['password'])
		if not user:
			raise ValidationError('user not found')
		return user

class UserSerializer(serializers.ModelSerializer):
	likes_count = serializers.IntegerField(source='likes_received.count', read_only=True)

	class Meta:
		model = UserModel
		fields = ('user_id', 'email', 'name', 'image', 'likes_count')

class SingleUserSerializer(serializers.ModelSerializer):
	likes_count = serializers.IntegerField(source='likes_received.count', read_only=True)

	class Meta:
		model = UserModel
		fields = ('user_id', 'email', 'name', 'image', 'likes_count')
