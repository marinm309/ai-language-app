from django.urls import path
from .views import ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView, FavoriteAPIView

urlpatterns = [
    path('', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('<int:pk>', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-retrieve-update-destroy'),
    path('favorite/<int:pk>', FavoriteAPIView.as_view(), name='favorite'),
]
