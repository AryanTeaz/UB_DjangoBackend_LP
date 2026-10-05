from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('low-stock/', views.low_stock_list, name='low-stock-list'),
    path('html/products/', views.product_list_html, name='product-list-html'),
]