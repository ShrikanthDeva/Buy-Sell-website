from django.contrib import admin
from django.urls import path
from . import views


app_name = 'myapp'
urlpatterns = [
    path('',views.index),
    path('products/',views.products,name='products'),
    path('products/<int:id>/',views.product_details,name='product_details'),
    path('products/add/',views.add_product,name='add_product'),
    path('update/<int:id>/',views.update_product,name='update_product'),
    path('delete/<int:id>/',views.delete_product,name='delete_product'),
    
]

