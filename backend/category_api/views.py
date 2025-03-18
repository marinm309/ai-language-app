from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Category
from .serializers import CategorySerializer

class CategoryAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)