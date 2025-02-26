from django.urls import path
from .views import index, product_detail, all_products, category_products

urlpatterns = [
    path('', index, name='home'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('all-products/', all_products, name='all_products'),
    path('category/<slug:category_slug>/', category_products, name='category_products'),
]
