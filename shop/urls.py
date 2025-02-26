from django.urls import path
from .views import product_detail, all_products
from shop import views

urlpatterns = [
    path('home/',views.index, name='index'),
    path('product-detail/<int:product_id>/', product_detail, name='product_detail'),
    path('all-products/', all_products, name='all_products'),
    path('category/<slug:category_slug>/', category_products, name='category_products'),

]
