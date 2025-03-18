from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Product, Favorite
from .serializers import ProductSerializer, FavoriteSerializer

class ProductListCreateAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request):
        category = request.query_params.get('category', None)
        profile = request.query_params.get('profile', None)
        total_results = request.query_params.get('total_results', None)
        search = request.query_params.get('search', None)
        if category:
            products = Product.objects.filter(category__name=category)
        elif profile:
            products = Product.objects.filter(user__user_id=profile)
        elif total_results:
            products = Product.objects.all()[Product.objects.count() - int(total_results):]
        elif search:
            products = Product.objects.filter(title__icontains=search)
        else:
            products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FavoriteAPIView(APIView):


    def get(self, request, pk):
        favorite = get_object_or_404(Favorite, pk=pk)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

        if not created:
            return Response({"detail": "You have already put that in favorite."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "You put that in favorite."}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        Favorite.objects.filter(user=request.user, product=product).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)