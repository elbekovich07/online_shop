from django.urls import path
from .views import product_detail
from shop import views

urlpatterns = [
    path('home/',views.index, name='index'),
    path('product-detail/<int:product_id>/', product_detail, name='product_detail'),
]
