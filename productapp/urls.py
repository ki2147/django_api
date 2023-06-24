from django.urls import path
from .views import ProductListAPIView, ProductDetailView

app_name = 'productapp'

urlpatterns = [
    path('api/products/<int:pk>', ProductDetailView.as_view(), name='product-detail-view'),
    path('api/products/', ProductListAPIView.as_view(), name='product-view'),
]
