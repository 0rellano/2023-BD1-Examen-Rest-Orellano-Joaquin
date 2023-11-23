from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

from api.models import Customers, Categories, Employees, Suppliers, Shippers, Orders, Orderdetails, Products
from api.serializers import CustomersSerializer, CategoriesSerializer, EmployeesSerializer, SuppliersSerializer, ShippersSerializer, OrdersSerializer, OrderdetailsSerializer, ProductsSerializer

def index(request):
    return HttpResponse("Hello, world. You're at dea hablaba en ingles el loco")


class BaseView(APIView):
    model = None
    serializer = None

    def get(self, request):
        queryset = self.model.objects.all()
        serializer = self.serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BaseIdView(APIView):
    model = None
    serializer = None
    field_pk = None

    def get_object(self, pk):
        try:
            return self.model.objects.get(**{self.field_pk: pk})
        except self.model.DoesNotExist:
            raise Http404("Object does not exist.")
        
    def get(self, request, pk):
        instance = self.get_object(pk)
        serializer = self.serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = self.serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        instance = self.get_object(pk)
        serializer = self.serializer(instance)
        instance.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)


class customers(BaseView):
    model = Customers
    serializer = CustomersSerializer

class customers_id(BaseIdView):
    model = Customers
    serializer = CustomersSerializer
    field_pk = 'customerid'


class categories(BaseView):
    model = Categories
    serializer = CategoriesSerializer

class categories_id(BaseIdView):
    model = Categories
    serializer = CategoriesSerializer
    field_pk = 'categoryid'

class employyes(BaseView):
    model = Employees
    serializer = EmployeesSerializer

class employyes_id(BaseIdView):
    model = Employees
    serializer = EmployeesSerializer
    field_pk = 'employeeid'

class products(BaseView):
    model = Products
    serializer = ProductsSerializer

class products_id(BaseIdView):
    model = Products
    serializer = ProductsSerializer
    field_pk = 'productid'

class suppliers(BaseView):
    model = Suppliers
    serializer = SuppliersSerializer

class suppliers_id(BaseIdView):
    model = Suppliers
    serializer = SuppliersSerializer
    field_pk = 'supplierid'

class shippers(BaseView):
    model = Shippers
    serializer = ShippersSerializer

class shippers_id(BaseIdView):
    model = Shippers
    serializer = ShippersSerializer
    field_pk = 'shipperid'

class orders(BaseView):
    model = Orders
    serializer = OrdersSerializer

class orders_id(BaseIdView):
    model = Orders
    serializer = OrdersSerializer
    field_pk = 'orderid'

class orderdetails(BaseView):
    model = Orderdetails
    serializer = OrderdetailsSerializer

def orderdetail_id(request, orderid, productid):
    try:
        orderDetail = Orderdetails.objects.get(orderid=orderid, productid=productid)
    except Orderdetails.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = OrderdetailsSerializer(orderDetail)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = OrderdetailsSerializer(orderDetail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        orderDetail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
      
@api_view(['GET'])
def prueba1(request):
	orders = Orders.objects.all()
	if request.GET.get('fechaMayor') and request.GET.get('fechaMenor'):
		orders = Orders.objects.filter(orderdate__range=(request.GET.get('fechaMenor'), request.GET.get('fechaMayor')))
	else:
		if request.GET.get('fechaMayor'):
			orders = orders.filter(orderdate__gt=request.GET.get('fechaMayor'))
		if request.GET.get('fechaMenor'):
			orders = orders.filter(orderdate__gt=request.GET.get('fechaMenor'))
	serializer = OrdersSerializer(orders, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)

def prueba2(request):
		customers = Customers.objects.all()
		if request.GET.get('comienza'):
			customers.filter(contactname__startswith)=request.GET.get('comienza'))
		if request.GET.get('termina'):
			customers.filter(contactname__endswith)=request.GET.get('termina'))
		if request.GET.get('contiene'):
			customers.filter(contactname__contains)=request.GET.get('contiene'))
		serializer = CustomersSerializer(customers, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

