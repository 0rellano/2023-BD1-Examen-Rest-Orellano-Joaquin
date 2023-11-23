from django.urls import path
from api.views import index, customers, customers_id, categories, categories_id, employyes, employyes_id, suppliers, suppliers_id, shippers, shippers_id, orders, orders_id, orderdetails, orderdetail_id, products, products_id
from api.views import prueba_endpoint1, prueba_endpoint2

urlpatterns = [
    path('', index),
    path('customers/', customers.as_view()),
    path('customers/<str:pk>/', customers_id.as_view()),
    path('categories/', categories.as_view()),
    path('categories/<int:pk>/', categories_id.as_view()),
    path('employees/', employyes.as_view()),
    path('employees/<int:pk>/', employyes_id.as_view()),
    path('suppliers/', suppliers.as_view()),
    path('suppliers/<int:pk>/', suppliers_id.as_view()),
    path('shippers/', shippers.as_view()),
    path('shippers/<int:pk>/', shippers_id.as_view()),
    path('orders/', orders.as_view()),
    path('orders/<str:int>/', orders_id.as_view()),
    path('products/', products.as_view()),
    path('products/<int:pk>/', products_id.as_view()),
    path('orderdetails/', orderdetails.as_view()),
    path('orderdetails/<int:orderid>/<int:productid>/', orderdetail_id),

    path('prueba_endpoint1/', prueba_endpoint1),
    path('prueba_endpoint2/', prueba_endpoint2),

]