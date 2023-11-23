from django.urls import path
from api.views import index, customers, customers_id, categories, categories_id, employyes, employyes_id, suppliers, suppliers_id, shippers, shippers_id, orders, orders_id, orderdetails, orderdetail_id, products, products_id


urlpatterns = [
    path('', index),
    path('customers/', customers.as_view()),
    path('customers/<str:pk>/', customers_id.as_view()),
    path('categories', categories.as_view()),
    path('categories/<str:pk>/', categories_id.as_view()),
    path('employees/', employyes.as_view()),
    path('employees/<str:pk>/', employyes_id.as_view()),
    path('suppliers/', suppliers.as_view()),
    path('suppliers/<str:pk>/', suppliers_id.as_view()),
    path('shippers/', shippers.as_view()),
    path('shippers/<str:pk>/', shippers_id.as_view()),
    path('orders/', orders.as_view()),
    path('orders/<str:pk>/', orders_id.as_view()),
    path('products/', products.as_view()),
    path('products/<str:pk>/', products_id.as_view()),
    path('orderdetails/', orderdetails.as_view()),
    path('orderdetails/<str:pk>/', orderdetail_id),
]