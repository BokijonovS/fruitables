from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('products/', AllProductList.as_view(), name='all_products'),
    path('product/<slug:slug>/', detail, name='detail'),
    path('products/<str:category_slug>/', all_products_by_category, name='products_by_category'),
    path('rate/<int:product_id>/<int:rating>/', rate),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('save-review/<slug:product_slug>/', save_review, name='save_review'),
    path('discounts/', ByDiscount.as_view(), name='discounts'),
    path('cart/', cart, name='cart'),
    path('to-cart/<int:product_id>/<str:action>', to_cart, name='to_cart'),
    path('checkout/', checkout, name='checkout'),

]
