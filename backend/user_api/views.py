from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, SingleUserSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from django.contrib.auth import get_user_model

from django.middleware.csrf import get_token

UserModel = get_user_model()

class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		email = request.data.get('email')
		if UserModel.objects.filter(email=email).exists():
			return Response({'error': 'Email already taken'}, status=status.HTTP_400_BAD_REQUEST)
	
		clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			if user:
				login(request, user)
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	
	def post(self, request):
		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()

	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	
	def delete(self, request):
		user = request.user
		user.delete()
		return Response({'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
	
	def get(self, request):
		user = request.user
		csrf_token = get_token(request)
		serializer = UserSerializer(user)
		return Response({'user': serializer.data, 'csrf_token': csrf_token}, status=status.HTTP_200_OK)
	

class SingleUserView(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()

	def get(self, request, pk):
		user = UserModel.objects.get(user_id=pk)
		serializer = SingleUserSerializer(user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class AllUsersView(APIView):
	def get(self, request):
		users = UserModel.objects.all()
		serializer = UserSerializer(users, many=True)
		
		return Response(serializer.data)
